using System;

namespace DesignPatterns.Mediator
{
    public class Aircraft : BaseComponent
    {
        public string Name { get; private set; }
        public bool IsTakingOff { get; set; }
        public bool IsLanded { get; private set; }

        public Aircraft(string name, IMediator mediator = null) : base(mediator)
        {
            Name = name;
            IsTakingOff = false;
            IsLanded = false;
        }


        public void RequestLanding()
        {
            if (IsLanded)
            {
                Console.WriteLine($"Aircraft {Name} is already landed.");
                return;
            }

            Console.WriteLine($"Aircraft {Name} is requesting landing permission.");

            if (_mediator != null)
            {
                bool canLand = _mediator.RequestLanding(this);
                if (canLand)
                {
                    IsLanded = true;
                    Console.WriteLine($"Aircraft {Name} has landed successfully.");
                }
                else
                {
                    Console.WriteLine($"Aircraft {Name} cannot land - no available runway.");
                }
            }
        }

        public void RequestTakeOff()
        {
            if (!IsLanded)
            {
                Console.WriteLine($"Aircraft {Name} is not on the ground.");
                return;
            }

            Console.WriteLine($"Aircraft {Name} is requesting takeoff permission.");
            IsTakingOff = true;

            if (_mediator != null)
            {
                bool canTakeOff = _mediator.RequestTakeOff(this);
                if (canTakeOff)
                {
                    IsLanded = false;
                    IsTakingOff = false;
                    Console.WriteLine($"Aircraft {Name} has taken off successfully.");
                }
                else
                {
                    IsTakingOff = false;
                    Console.WriteLine($"Aircraft {Name} cannot take off at this moment.");
                }
            }
        }
    }
}