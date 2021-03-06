#pragma once



#ifdef __cplusplus
namespace lib_gpu {
extern "C" {
#endif
    struct NVIDIA_DELTA_ENTRY;

    enum GPU_OVERCLOCK_SETTING_AREA
    {
        GPU_OVERCLOCK_SETTING_AREA_CORE,
        GPU_OVERCLOCK_SETTING_AREA_MEMORY,
        GPU_OVERCLOCK_SETTING_AREA_SHADER,
        GPU_OVERCLOCK_SETTING_AREA_OVERVOLT,
        GPU_OVERCLOCK_SETTING_AREA_POWER_LIMIT,
        GPU_OVERCLOCK_SETTING_AREA_THERMAL_LIMIT,
    };

    struct GpuOverclockSetting
    {
        bool editable;
        float currentValue;
        float minValue;
        float maxValue;
#ifdef __cplusplus
        GpuOverclockSetting();
        GpuOverclockSetting(float min, float current, float max, bool editable = false);
        GpuOverclockSetting(NVIDIA_DELTA_ENTRY const& delta, bool editable = false);
#endif
    };

    struct GpuOverclockFlag
    {
        bool editable;
        bool value;
    };

    struct GpuOverclockProfile
    {
#ifdef __cplusplus
        const GpuOverclockSetting& operator[](const GPU_OVERCLOCK_SETTING_AREA area) const;
#endif
        GpuOverclockSetting coreOverclock;
        GpuOverclockSetting memoryOverclock;
        GpuOverclockSetting shaderOverclock;
        GpuOverclockSetting overvolt;
        GpuOverclockSetting powerLimit;
        GpuOverclockSetting thermalLimit;
        GpuOverclockFlag thermalLimitPriority;
    };

    struct GpuUsage
    {
        float coreUsage;
        float fbUsage;
        float vidUsage;
        float busUsage;
    };

    struct GpuClocks
    {
        float coreClock;
        float memoryClock;
        float shaderClock;
    };
#ifdef __cplusplus
}
}
#endif