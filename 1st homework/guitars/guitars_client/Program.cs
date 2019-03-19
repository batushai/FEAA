using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;

namespace guitars_client
{
    class Program
    {
        static void Main(string[] args)
        {
            TcpClient client = new TcpClient("127.0.0.1", 5000);
            NetworkStream stream = client.GetStream();
            while(true)
            {
                Console.Write("Search:");
                String search_text = Console.ReadLine();

                //config connection
                byte[] bytesToSend = Encoding.ASCII.GetBytes(search_text);
                stream.Write(bytesToSend, 0, bytesToSend.Length);

                //recieve response
                byte[] buffer = new byte[client.ReceiveBufferSize];
                int n_bytes = stream.Read(buffer, 0, client.ReceiveBufferSize);
                string response = Encoding.ASCII.GetString(buffer, 0, n_bytes);
                Console.WriteLine("Response: " + response);
            }
        }
    }
}
