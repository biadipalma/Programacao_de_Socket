import java.io.*; 
import java.net.*; 

class TCPServer { 

  public static void main(String argv[]) throws Exception 
    { 
      String clientSentence; 
      String capitalizedSentence; 

      ServerSocket welcomeSocket = new ServerSocket(6789); 
  
      while(true) { 
  
           Socket connectionSocket = welcomeSocket.accept(); 
           System.out.println("trafego " + connectionSocket.getTrafficClass() ); 
           System.out.println("Socket Remoto " + connectionSocket.getRemoteSocketAddress() ); 
           
           BufferedReader inFromClient = 
              new BufferedReader(new
              InputStreamReader(connectionSocket.getInputStream())); 

           DataOutputStream  outToClient = 
             new DataOutputStream(connectionSocket.getOutputStream()); 

           clientSentence = inFromClient.readLine(); 
           
           System.out.println("recebido" + connectionSocket.getOutputStream()  );
            
           capitalizedSentence = clientSentence.toUpperCase() + '\n'; 
           

           outToClient.writeBytes(capitalizedSentence); 
        } 
    } 
} 
