using System;

namespace DesignPatterns.Mediator
{
    public class Runway : BaseComponent
    {
        public readonly Guid Id = Guid.NewGuid();
        public Aircraft OccupiedByAircraft { get; private set; }
        public bool IsBusy => OccupiedByAircraft != null;

        public Runway(IMediator mediator = null) : base(mediator)
        {
        }

        public bool TryOccupy(Aircraft aircraft)
        {
            if (IsBusy)
            {
                return false;
            }

            OccupiedByAircraft = aircraft;
            HighlightRed();
            _mediator?.NotifyRunwayStatusChanged(this);
            return true;
        }

        public bool TryRelease(Aircraft aircraft)
        {
            if (OccupiedByAircraft != aircraft)
            {
                return false;
            }

            OccupiedByAircraft = null;
            HighlightGreen();
            _mediator?.NotifyRunwayStatusChanged(this);
            return true;
        }
        public bool CheckIsActive()
        {
            return IsBusy && OccupiedByAircraft.IsTakingOff;
        }

        private void HighlightRed()
        {
            Console.WriteLine($"Runway {Id:N}[0..7] is now BUSY!");
        }

        private void HighlightGreen()
        {
            Console.WriteLine($"Runway {Id:N}[0..7] is now FREE!");
        }
    }
}