# Install Python packages
`pip3 install -r requirements.txt`

# To run the program
The program runs automatically when the raspberry pi is turned on. However, you could also turn it on manually by running
```
sh ./launcher.py
```

# To kill the program
Just look up for the program `start.py` in the processes and kill it
```
ps aux | egrep "[s]tart.py"
kill -9 ${PID_FROM_ABOVE}
```