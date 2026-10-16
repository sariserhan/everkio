#import <Foundation/Foundation.h>
#include <TargetConditionals.h>

extern "C" int EverkioReadThermalState()
{
#if TARGET_OS_SIMULATOR
    // Simulator thermals cannot establish physical iPhone thermal behavior.
    return -1;
#else
    switch ([NSProcessInfo processInfo].thermalState)
    {
        case NSProcessInfoThermalStateNominal: return 0;
        case NSProcessInfoThermalStateFair: return 1;
        case NSProcessInfoThermalStateSerious: return 2;
        case NSProcessInfoThermalStateCritical: return 3;
        default: return -1;
    }
#endif
}
