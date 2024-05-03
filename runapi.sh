#!/bin/bash
#--------------------------------------
# Script: runapi.sh
# Purpose: run api backend for kanik camer simple
# Author: hawat
# Date: 2024-05-01
# Version: 0.9
#--------------------------------------


uvicorn api:app --reload --host 0.0.0.0 --port 8000