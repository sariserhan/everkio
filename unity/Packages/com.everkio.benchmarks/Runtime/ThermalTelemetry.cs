using System.Runtime.InteropServices;

namespace Everkio.Benchmarks
{
    public static class ThermalTelemetry
    {
        // Values are the Everkio native bridge contract, not an OS enum cast.
        public enum State { Unknown = -1, Nominal = 0, Fair = 1, Serious = 2, Critical = 3 }

#if UNITY_IOS && !UNITY_EDITOR
        [DllImport("__Internal")]
        private static extern int EverkioReadThermalState();
        public const string Method = "ios_nsprocessinfo_thermalstate_per_update";
#else
        public const string Method = "unavailable";
#endif

        public static State Read()
        {
#if UNITY_IOS && !UNITY_EDITOR
            int value = EverkioReadThermalState();
            return value >= 0 && value <= 3 ? (State)value : State.Unknown;
#else
            return State.Unknown;
#endif
        }

        public static string Name(State state)
        {
            switch (state)
            {
                case State.Nominal: return "nominal";
                case State.Fair: return "fair";
                case State.Serious: return "serious";
                case State.Critical: return "critical";
                default: return "unknown";
            }
        }
    }
}
