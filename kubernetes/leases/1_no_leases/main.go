package main

import (
	"os"
	"time"

	"github.com/sirupsen/logrus"
)

var log = logrus.New()
var INTERVAL_TIME = 3 * time.Second

func start_service(){
	log.Info("Service init process")
	log.Info("Service loop starting")
	for{
		service_loop()
		time.Sleep(INTERVAL_TIME)
	}
}

func service_loop(){
	log.Info("I'm the leader! running changes")
}

func init() {
	log.SetFormatter(&logrus.JSONFormatter{
		TimestampFormat: "2006-01-02T15:04:05.000Z07:00",
	})
	log.SetLevel(logrus.InfoLevel)
}

func main() {
	hostname, err := os.Hostname()
	if err != nil {
		log.Fatal(err)
	}

	log.WithFields(logrus.Fields{
		"hostname": hostname,
	}).Info("Service Starting on hostname")
	start_service()
}