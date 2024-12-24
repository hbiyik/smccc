#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>

#include "smccc.h"


static long smccc_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    struct arm_smccc_ioctl data;
    if (cmd == IOCTL_CMD_SMCCC) {
        if (copy_from_user(&data, (void __user *)arg, sizeof(struct arm_smccc_ioctl)))
            return -EFAULT;

        arm_smccc_smc(data.req.id,
                      data.req.arg0, data.req.arg1, data.req.arg2,
                      0, 0, 0, 0, &data.res);
        if (copy_to_user((void __user *)arg, &data, sizeof(struct arm_smccc_ioctl)))
            return -EFAULT;

        return 0;
    }

    return -EINVAL;
}

struct proc_ops SMCCC_FOPS = {
    .proc_ioctl = smccc_ioctl,
};


static void smccc_exit(void){
    remove_proc_entry(DEVICE_NAME, NULL);
    // TODO: free
    printk(KERN_INFO "%s: module unloaded\n", __func__);
}

static int smccc_init(void){
    if (!proc_create(DEVICE_NAME, 0, NULL, &SMCCC_FOPS)) {
        printk(KERN_WARNING "%s: cannot create procfs device\n", __func__);
        goto fail;
    }

    printk(KERN_INFO "%s: module loaded\n", __func__);
    return 0;

fail:
    smccc_exit();
    return -ENOENT;
}


module_init(smccc_init);
module_exit(smccc_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Boogie <boogiepop@gmx.com>");
MODULE_DESCRIPTION("ARM SMCCC IOCTL Interface driver");
MODULE_VERSION("0.1");
