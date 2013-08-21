"Sleep for a random amount of time"
from random import normalvariate
from time import sleep

SLEEP={
  "mu":8
, "sigma":4
}

def randomsleep(mean=SLEEP['mu'],sd=SLEEP['sigma']):
  seconds=normalvariate(mean,sd)
  if seconds>0:
    sleep(seconds)