using System;
using System.Collections.Generic;
using System.Linq;

namespace DesignPatterns.Mediator
{
    public class CommandCentre : IMediator
    {
        private List<Runway> _runways = new List<Runway>();
        private List<Aircraft> _aircrafts = new List<Aircraft>();

        public CommandCentre(Runway[] runways, Aircraft[] aircrafts)
        {
            _runways.AddRange(runways);
            _aircrafts.AddRange(aircrafts);

            foreach (var runway in _runways)
            {
                runway.SetMediator(this);
            }

            foreach (var aircraft in _aircrafts)
            {
                aircraft.SetMediator(this);
            }
        }

        public bool RequestLanding(Aircraft aircraft)
        {
            Console.WriteLine($"Command Centre: Processing landing request from {aircraft.Name}");

            var availableRunway = _runways.FirstOrDefault(r => !r.IsBusy);

            if (availableRunway != null)
            {
                Console.WriteLine($"Command Centre: Assigning runway {availableRunway.Id:N}[0..7] to {aircraft.Name}");
                return availableRunway.TryOccupy(aircraft);
            }

            Console.WriteLine($"Command Centre: No available runways for {aircraft.Name}");
            return false;
        }

        public bool RequestTakeOff(Aircraft aircraft)
        {
            Console.WriteLine($"Command Centre: Processing takeoff request from {aircraft.Name}");

            var occupiedRunway = _runways.FirstOrDefault(r => r.OccupiedByAircraft == aircraft);

            if (occupiedRunway != null)
            {
                Console.WriteLine($"Command Centre: Clearing runway {occupiedRunway.Id:N}[0..7] for {aircraft.Name}");
                return occupiedRunway.TryRelease(aircraft);
            }

            Console.WriteLine($"Command Centre: Cannot find runway occupied by {aircraft.Name}");
            return false;
        }

        public void NotifyRunwayStatusChanged(Runway runway)
        {
            string status = runway.IsBusy ? "OCCUPIED" : "FREE";
            string aircraftInfo = runway.IsBusy ? $" by {runway.OccupiedByAircraft.Name}" : "";
            Console.WriteLine($"Command Centre: Runway {runway.Id:N}[0..7] is now {status}{aircraftInfo}");
        }

        public void ShowStatus()
        {
            Console.WriteLine("\n=== AIRPORT STATUS ===");
            Console.WriteLine($"Total Runways: {_runways.Count}");
            Console.WriteLine($"Total Aircraft: {_aircrafts.Count}");

            Console.WriteLine("\nRunways:");
            foreach (var runway in _runways)
            {
                string status = runway.IsBusy ? $"BUSY (occupied by {runway.OccupiedByAircraft.Name})" : "FREE";
                Console.WriteLine($"Runway {runway.Id:N}[0..7]: {status}");
            }

            Console.WriteLine("\nAircraft:");
            foreach (var aircraft in _aircrafts)
            {
                string status = aircraft.IsLanded ? "LANDED" : "AIRBORNE";
                if (aircraft.IsTakingOff) status += " (TAKING OFF)";
                Console.WriteLine($"  {aircraft.Name}: {status}");
            }
            Console.WriteLine("========================\n");
        }
    }
}