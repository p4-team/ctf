(ns main
  (:require [clojure.java.shell :as shell])
  (:gen-class))

;; We want to be sure none of our calls relies on reflection.
(set! *warn-on-reflection* 1)


(defmulti option identity)
(defmethod option "1" [_]
  (try
    (-> (read-line)
        (read-string))
    (println "Good job, you know how to balance brackets. Now go, get the flag.")
    (catch Exception e
      (println "You need to work on your balancing skills."))))

(defmethod option "2" [_]
  (println "Exiting.")
  (System/exit 0))

(defmethod option :default [_]
  (println "Invalid choice."))

(defn- print-options []
  (println "1: Send string")
  (println "2: Exit"))


(defn- get-graal-version []
  (->> (clojure.java.shell/sh "native-image" "--version")
       :out
       clojure.string/trim-newline
       (re-find #"\d.\d.\d-\w+")))

(defn -main []
  (println "Welcome to HolyGraal version" (get-graal-version))
  (println "Everybody knows that keeping track of brackets is hard in LISP languages.")
  (println "We now introduce: verify brackets as a service.")
  (print-options)
  (loop [input (read-line)]
    (option input)
    (print-options)
    (recur (read-line))))

// #=(println #=(clojure.java.shell/sh "cat" "flag.txt"))

