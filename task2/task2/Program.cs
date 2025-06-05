using System;

namespace DesignPatterns.Mediator
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Air Traffic Control System - Mediator Pattern Demo");
            Console.WriteLine("====================================================\n");

            var runways = new Runway[]
            {
                new Runway(),
                new Runway(),
                new Runway()
            };

            var aircrafts = new Aircraft[]
            {
                new Aircraft("Boeing 747"),
                new Aircraft("Airbus A380"),
                new Aircraft("Cessna 172"),
                new Aircraft("Boeing 737"),
                new Aircraft("Airbus A320")
            };

            var commandCentre = new CommandCentre(runways, aircrafts);

            commandCentre.ShowStatus();

            Console.WriteLine("SCENARIO 1: Aircraft Landing");
            Console.WriteLine("================================");
            aircrafts[0].RequestLanding(); 
            aircrafts[1].RequestLanding(); 
            aircrafts[2].RequestLanding(); 
            aircrafts[3].RequestLanding(); 
            aircrafts[4].RequestLanding(); 

            commandCentre.ShowStatus();

            Console.WriteLine("SCENARIO 2: Aircraft Takeoff");
            Console.WriteLine("===============================");
            aircrafts[1].RequestTakeOff(); 
            aircrafts[4].RequestLanding(); 

            commandCentre.ShowStatus();

            Console.WriteLine("SCENARIO 3: Invalid Operations");
            Console.WriteLine("=================================");
            aircrafts[1].RequestTakeOff(); 
            aircrafts[0].RequestLanding(); 

            commandCentre.ShowStatus();

            Console.WriteLine("Demo completed! Press any key to exit...");
            Console.ReadKey();
        }
    }
}