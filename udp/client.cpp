//list of header files to load
#include <iostream>     // input,output stream handling
#include <cstring>      // string related operation
#include <arpa/inet.h>  //main header for internet related operations
#include <unistd.h>     //stadard symbolic constants
#include <fstream>      //main header for file operation
#include <ctime>        //used for date and time operationa
#include <sstream>      //stream class for srtrings

// use names for objects and variables from the standard library
using namespace std;

// log file for all the events client
ofstream logFile;

//this function simoultaneously sends the messages to stdout as well as logfile
void logMessage(const string& source,const string& message) {
    time_t now = time(nullptr);
    char timeStr[100];
    strftime(timeStr, sizeof(timeStr), "[%Y-%m-%d %H:%M:%S]", localtime(&now));
    //sending the output string to std out
    cout << timeStr << " "<< source << ": " << message << endl;
    //sending the output string to log file
    logFile << timeStr << " " << source << ": " << message << endl;
}

int main() {
    //  IP address of the server
    const char* SERVER_IP = "127.0.0.1";
    const int PORT = 8080;
    const int BUFFER_SIZE = sizeof(unsigned long long);

    // Open client log file
    logFile.open("client_log.txt", ios::app);
    if (!logFile.is_open()) {
        cerr << "Error opening log file" << endl;
        return 1;
    }

    logMessage("Client", "Client started");

    // Creating a UDP socket
    int clientSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (clientSocket == -1) {
        logMessage("Client", "Error creating socket");
        logFile.close();
        return 1;
    }

    // Server address
    sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    inet_pton(AF_INET, SERVER_IP, &(serverAddr.sin_addr));

    //opening the input file
    fstream fh;
    fh.open("hw6input.txt",ios::in);
    // error handling in the event of failure to open file
    if(!fh.is_open())
    {
        logMessage("Client", "Error opening input file");
        logFile.close();
        return 1;
    }

    string line;
    while(getline(fh,line))
    {
        istringstream iss(line);
        // Converts hexadecimal string to an unsigned long long using istringstream and hex.
        unsigned long long intValue;
        if (iss >> hex >> intValue) {
            // Conversion successful, send the value to the server
            if (sendto(clientSocket, &intValue, BUFFER_SIZE, 0, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
                logMessage("Client", "Error sending message to the server");
                break;  // Exit the loop in case of an error
            }
            logMessage("Client","Sent integer to server: " + to_string(intValue));

            // Set up a timeout for 10 seconds to wait for a response from the server
            fd_set readSet;
            FD_ZERO(&readSet);
            FD_SET(clientSocket, &readSet);

            struct timeval timeout;
            timeout.tv_sec = 10;
            timeout.tv_usec = 0;

            int readySockets = select(clientSocket + 1, &readSet, nullptr, nullptr, &timeout);

            if (readySockets == -1) {
                logMessage("Client", "Error in select function");
                break;
            } else if (readySockets == 0) {
                logMessage("Client", "Error: Server did not respond within 10 seconds");
                break;
            }

            // Server responded, receive the message
            char buffer[BUFFER_SIZE];
            sockaddr_in serverResponseAddr;
            socklen_t serverResponseAddrLen = sizeof(serverResponseAddr);

            int bytesReceived = recvfrom(clientSocket, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&serverResponseAddr, &serverResponseAddrLen);
            if (bytesReceived == -1) {
                logMessage("Client", "Error receiving response from the server");
                break;
            }

            logMessage("Client", "Received response from server: " + string(buffer));
	    sleep(10);
        } else {
            // Conversion failed, handle the error
            logMessage("Client"," Error converting hex string to integer: " + line);
        }
    }

    //close the file
    fh.close();

    // Close the socket
    close(clientSocket);

    // close the log file
    logFile.close();

    return 0;
}
