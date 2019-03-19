using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;

namespace guitars
{
    class Program
    {
        public  class Guitar
        {
            public string name;
            public string colors;
            public Guitar(string n, string co)
            {
                name = n;
                colors = co;
            }
        }

        static void Main(string[] args)
        {
            List<Guitar> DB = new List<Guitar>();
            //Hardcoding guitars to the DB
            DB.Add(new Guitar("Gibson", "Yellow Green Sunburst Green Red"));
            DB.Add(new Guitar("Harley Benton", "Orange Copper Green Graphic Gold"));
            DB.Add(new Guitar("Jackson", "Blue Brown Graphic Black Yellow"));
            DB.Add(new Guitar("Ibanez", "Copper Gold Brown"));
            DB.Add(new Guitar("Schecter", "Natural Red Black Grey"));
            DB.Add(new Guitar("Epiphone", "Brown Grey Copper Purple Gold Silver"));
            DB.Add(new Guitar("Fender", "Silver Natural"));
            DB.Add(new Guitar("ESP", "Orange Purple Green Graphic"));
            DB.Add(new Guitar("Dean Guitars", "Silver Brown Yellow Copper"));
            DB.Add(new Guitar("PRS", "Black Blue Natural"));

            //ip, port on which clients can connect to
            //config part
            System.Net.IPAddress server_ip = System.Net.IPAddress.Parse("127.0.0.1");
            TcpListener listener = new TcpListener(server_ip, 5000);
            listener.Start();
            Console.WriteLine("Server started on 127.0.0.1:5000");
            //the client object
            TcpClient client = listener.AcceptTcpClient();

            while (true)
            {
                //receive
                NetworkStream stream = client.GetStream();
                byte[] buffer = new byte[client.ReceiveBufferSize];
                int n_bytes = stream.Read(buffer, 0, client.ReceiveBufferSize);
                string guitar_name = Encoding.ASCII.GetString(buffer, 0, n_bytes);

                //Searching in DB
                guitar_name = guitar_name.ToLower(); //converting to lowercase to search
                Console.WriteLine("Searching " + guitar_name);
                string response = "Guitar not found.";
                foreach (Guitar g in DB)
                {
                    string guitar_db = g.name.ToLower();
                    if (guitar_db.Equals(guitar_name))
                        response = guitar_name + " found." + '\n' + "Colors: " + g.colors;
                }

                //Sending the response back to client
                buffer = Encoding.ASCII.GetBytes(response);
                stream.Write(buffer, 0, response.Length);
            }
        }
    }
}
