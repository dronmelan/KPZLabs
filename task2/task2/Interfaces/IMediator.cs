namespace DesignPatterns.Mediator
{
    public interface IMediator
    {
        bool RequestLanding(Aircraft aircraft);

        bool RequestTakeOff(Aircraft aircraft);

        void NotifyRunwayStatusChanged(Runway runway);
    }
}