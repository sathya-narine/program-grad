These are some important information to run client server program.

1. server.cpp has to compiled and executable name should be server. This can be achieved by
   g++ server.cpp -o server 
2. Server has to be started first.
   ./server 
3. client.cpp has to be compiled to clinet
   g++ client.cpp -o client 
4. Run the client to send message to server.
   ./client
5. The input file hw6input.txt is already present. Additional input files input1.txt, input2.txt is included.
   To run with those files please change the filename with in client.cpp and recompile.
6. Server creates a log file named server_log.txt and Client creates a log file named client_log.txt
7. There is a script named test.sh which automates the testing, but few important changes has to be made before running the script.
8. g++ server.cpp -o server 
9. client_file_arg.cpp is a modified client which takes file name as an command line argument.
   g++ client_file_arg.cpp -o client_arg
10. Please note the executable names should only be server and client_arg for the script to run successfully.
11. chmod +x test.sh 
12. The script file expects a log file name as an input.
13. ./test.sh common_log.txt 
14. Consolidated log would be present in common_log.txt
15. sudo lsof -t -i:8080 | xargs kill -9 - use this command to reset port 8080
