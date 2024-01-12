//list of header files to load
#include <iostream>     // input,output stream handling
#include <cstring>      // string related operation
#include <arpa/inet.h>  //main header for internet related operations
#include <unistd.h>     //stadard symbolic constants
#include <ctime>        //used for date and time operations
#include <fstream>      //main header for file operation
#include <sstream>      //stream class for srtrings

//use names for objects and variables from the standard library
using namespace std;

// file stream for log file
ofstream logFile;

//this function simoultaneously sends the messages to stdout as well as logfile
void logMessage(const string& source,const string& message) {
    // current time
    time_t now = time(nullptr);
    char timeStr[100];
    // converts the date and time information
    strftime(timeStr, sizeof(timeStr), "[%Y-%m-%d %H:%M:%S]", localtime(&now));
    // sending the message to standard out
    cout << timeStr << " " << source << ": " << message << endl;
    // sending the message to log file
    logFile << timeStr << " " << source<< ": " << message << endl;
}

int main() {
    const int PORT = 8080;
    const int BUFFER_SIZE = sizeof(unsigned long long); // Using the same size as the client

    // Opening the log file
    logFile.open("server_log.txt", ios::app);
    if (!logFile.is_open()) {
        cerr << "Error opening log file" << endl;
        return 1;
    }

    // Create socket
    int serverSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (serverSocket == -1) {
        cerr << "Error creating socket" << endl;
        return 1;
    }

    // Bind socket to port 8080
    sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == -1)
    {
        logMessage("Server","Error binding socket");
        logFile.close();
        close(serverSocket);
        return 1;
    }

    logMessage("Server","Server started and listening on port 8080");

    // Receive and print messages
    char buffer[BUFFER_SIZE];
    sockaddr_in clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);

    while (true) {
        int bytesRead = recvfrom(serverSocket, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&clientAddr, &clientAddrLen);
        if (bytesRead == -1) {
            logMessage("Server","Error receiving message");
            break;
        }

        // converts the received data to an unsigned long long using memcpy
        unsigned long long receivedValue;
        memcpy(&receivedValue, buffer, BUFFER_SIZE);

        logMessage("Server", "Received message from client at IP " + string(inet_ntoa(clientAddr.sin_addr)) + ": " + to_string(receivedValue));

        // Send "Message received" back to the client
        const string responseMessage = "Message received by the server";
        int bytesSent = sendto(serverSocket, responseMessage.c_str(), responseMessage.size(), 0, (struct sockaddr*)&clientAddr, clientAddrLen);

        if (bytesSent == -1) {
            logMessage("Server", "Error sending response message to client");
            break;
        }
    }

    // Close the socket
    close(serverSocket);
    // close the log file
    logFile.close();
    return 0;
}
