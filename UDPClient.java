/*
 * Client App upon UDP
 * Weiying Zhu
 */ 
//Client: Server B, Server: Server A.
import java.io.*;
import java.net.*;
import java.util.*;

public class UDPClient {
    public static void main(String[] args) throws IOException {

        if (args.length != 1) {
	     //Input argument provides hostname?
             System.out.println("Usage: java UDPClient <hostname>");
             return;
        }

        // create a UDP socket, local port number, but will get assigned by the O.S., clients side, specifies where packets are delivered
        DatagramSocket udpSocket = new DatagramSocket();

	//Similar to scanner, creation of this instance reads user input
        BufferedReader sysIn = new BufferedReader(new InputStreamReader(System.in));
        String fromServer;
        String fromUser;
	
	// STEP 1 : READ USER INPUT
        while ((fromUser = sysIn.readLine()) != null) {
	  // return value of sys.InreadLine() of null indicates that an error occured, no string instance created
	  // when there is a system error, end the loop, close the socket
	  // If null is not returned, some input was entered, can even be an empty line
	  // If left empty, a string instance of an empty string was created

          //display user input
          System.out.println("From Client: " + fromUser);
			 
          // send request, convert characters to byte array, size determined by number of characters typed from user
          InetAddress address = InetAddress.getByName(args[0]);
	  byte[] buf = fromUser.getBytes();
          
	  // Datagram packet here is used to send information to the server side
	  //4 parameters, contents of byte array, size of array, destination IP address, and the destination port number (port num on servers side)
	  DatagramPacket udpPacket = new DatagramPacket(buf, buf.length, address, 5678); //P-Num
          // STEP 2: Call Send method to send instance of UDP Packet
	  udpSocket.send(udpPacket);
    
          // STEP 5: GET RESPONSE FROM SERVER
          byte[] buf2 = new byte[256];
          DatagramPacket udpPacket2 = new DatagramPacket(buf2, buf2.length);
          udpSocket.receive(udpPacket2);

          // display response
          fromServer = new String(udpPacket2.getData(), 0, udpPacket2.getLength());
          System.out.println("From Server: " + fromServer);
	  
	  // STEP 6: LOOP BACK TO STEP 1, UNTIL USER ENTERS "Bye." (One mpre cycle will still occur)
          if (fromUser.equals("Bye."))
              break;
        }
		  
        udpSocket.close();
    }
}


Now, it rejects the inital false input but accepts any subsequent bad inputs