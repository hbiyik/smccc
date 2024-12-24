#ifndef __SMCCC_DEFINE_H__
#define __SMCCC_DEFINE_H__

#include <linux/arm-smccc.h>

#define DEVICE_NAME "smccc"

struct arm_smccc_req {
    unsigned long id;
    unsigned long arg0;
    unsigned long arg1;
    unsigned long arg2;
};

struct arm_smccc_ioctl {
    struct arm_smccc_req req;
    struct arm_smccc_res res;
};

#define IOCTL_BASE 'A'
#define IOCTL_CMD_SMCCC _IOWR(IOCTL_BASE, 1, struct arm_smccc_ioctl)

#endif // __SMCCC_DEFINE_H__
