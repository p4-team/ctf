// +build !wasm
package main

import (
	"bytes"
	"context"
	"crypto/md5"
	"fmt"
	"github.com/golang/groupcache/lru"
	"github.com/golang/protobuf/proto"
	"log"
	"net/http"
	"os/exec"
	"strings"
	"sync"
	"time"
)

type validator struct {
	cache *lru.Cache
	lock  sync.Mutex
}

const validChars = "abcdefghijklmnopqrstuvwxuz.1234567890"

func checkAddress(address string) bool {
	valid := true
	for _, char := range address {
		if !strings.ContainsRune(validChars, char) {
			valid = false
		}
	}

	return valid
}

func md5bytes(data []byte) string {
	h := md5.New()
	h.Write(data)
	return string(h.Sum(nil))
}

func (v *validator) Valid(data []byte) *Command {
	if len(data) > 270 {
		return nil
	}

	key := md5bytes(data)
	v.lock.Lock()
	defer v.lock.Unlock()

	var cmd Command
	if err := proto.Unmarshal(data, &cmd); err != nil {
		return nil
	}

	var address string
	switch c := cmd.Command.(type) {
	case *Command_PingCommand:
		address = c.PingCommand.GetAddress()
	case *Command_TracerouteCommand:
		address = c.TracerouteCommand.GetAddress()
	}

	valid, ok := v.cache.Get(key)
	if ok && valid.(bool) {
		return &cmd
	} else if checkAddress(address) {
		v.cache.Add(key, true)
		return &cmd
	}
	return nil
}

func newValidator(entries int) *validator {
	return &validator{
		cache: lru.New(entries),
	}
}

func execute(cmd *Command) *ExecutionResult {
	var commandline string
	switch c := cmd.Command.(type) {
	case *Command_PingCommand:
		commandline = fmt.Sprintf("ping -%d -c %d %s", c.PingCommand.GetIpVersion(), c.PingCommand.GetCount(), c.PingCommand.GetAddress())
	case *Command_TracerouteCommand:
		commandline = fmt.Sprintf("traceroute -%d %s", c.TracerouteCommand.GetIpVersion(), c.TracerouteCommand.GetAddress())
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	e := exec.CommandContext(ctx, "/bin/sh", "-c", commandline)
	output, err := e.CombinedOutput()
	if err != nil {
		return &ExecutionResult{
			Result: &ExecutionResult_Error_{
				Error: &ExecutionResult_Error{
					Error: proto.String(err.Error()),
				},
			},
		}
	}

	return &ExecutionResult{
		Result: &ExecutionResult_Success_{
			Success: &ExecutionResult_Success{
				Output: output,
			},
		},
	}
}

func logHandler(handler http.Handler) http.Handler {
	if handler == nil {
		handler = http.DefaultServeMux
	}

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Println(r.RemoteAddr, r.Method, r.URL)
		handler.ServeHTTP(w, r)
	})
}

func main() {
	v := newValidator(10000)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("."))))
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "index.html")
	})
	http.HandleFunc("/command", func(w http.ResponseWriter, r *http.Request) {
		var buf bytes.Buffer
		_, err := buf.ReadFrom(r.Body)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		cmd := v.Valid(buf.Bytes())
		if cmd == nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		result := execute(cmd)
		data, err := proto.Marshal(result)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			return
		}

		w.Write(data)
	})

	http.ListenAndServe(":8080", logHandler(nil))
}
