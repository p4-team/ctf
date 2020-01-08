package main

import (
	"crypto/sha1"
	"fmt"
	"sync"
)

var sm sync.Map

type Thing struct {
	msg string
	t   int
}

type IPZeros struct {
	ip0 int
	ip1 int
	ip2 int
	ip3 int
}

func zeros(count int) string {
	b := ""
	for i := 0; i < count; i++ {
		b = b + "0"
	}
	return b
}

func countUndefined(b string) int {
	current := 0
	for _, c := range b {
		if c == 65533 {
			current++
		}
	}
	return current
}

func work2(id int, ips chan int) {
	for ipz := range ips {
		ip := "::" + zeros(ipz) + ":"
		for i := 1; i < 1000; i++ {
			ip1 := ip + zeros(i) + ":"
			for i2 := 1; i2 < 1000; i2++ {
				ip2 := ip1 + zeros(i2) + ":"
				for i3 := 1; i3 < 1000; i3++ {
					ip3 := ip2 + zeros(i3) + ":ffff:18.197.117.65"

					msg := ip3 + "|" + "cat flag.txt"
					digest := sha1.Sum([]byte(msg))
					b := string(digest[:])

					current := countUndefined(b)

					if current >= 19 {
						i, loaded := sm.LoadOrStore(b, Thing{msg, 1})
						if loaded && (i.(Thing)).t == 0 {
							thing := i.(Thing)
							fmt.Println("SUCCESS")
							fmt.Println(thing.msg)
							fmt.Println(msg)
						}
						fmt.Printf("ID %d found a match\n", id)
						fmt.Println(current)
						fmt.Println(ip3)
					}

				}
			}
		}

	}
}

func work(id int, ips chan int) {
	for ipz := range ips {
		ip := "::" + zeros(ipz) + ":"
		for i := 1; i < 1000; i++ {
			ip1 := ip + zeros(i) + ":"
			for i2 := 1; i2 < 1000; i2++ {
				ip2 := ip1 + zeros(i2) + ":"
				for i3 := 1; i3 < 1000; i3++ {
					ip3 := ip2 + zeros(i3) + ":ffff:18.197.117.65"
					fmt.Println(ip3)

					msg := ip3 + "|" + "ls -l"
					digest := sha1.Sum([]byte(msg))
					b := string(digest[:])

					current := countUndefined(b)

					if current >= 19 {
						i, loaded := sm.LoadOrStore(b, Thing{msg, 0})
						if loaded && (i.(Thing)).t == 1 {
							thing := i.(Thing)
							fmt.Println("SUCCESS")
							fmt.Println(thing.msg)
							fmt.Println(msg)
						}
						fmt.Printf("ID %d found a match\n", id)
						fmt.Println(current)
						fmt.Println(ip3)
					}

				}
			}
		}
	}
}

func main() {
	queue := make(chan int, 1000)
	queue2 := make(chan int, 1000)
	var wg sync.WaitGroup
	for i := 0; i < 18; i++ {
		wg.Add(1)
		go work(i, queue)
		wg.Add(1)
		go work2(i+10000, queue2)
	}
	for i0 := 1; i0 < 1000; i0++ {
		queue <- i0
		queue2 <- i0
	}
	wg.Wait()
}
