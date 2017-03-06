/*
 * 名称: rmdisk
 * 版本：1.1
 * 作者：james.feng
 * 日期：2016.3.22
 * 描述：一个管理外部存储设备的后台工具，可阻止任何外部存储设备接入计算机，以保障系统安全。
 * 更新：
 * 			1.去除了授权链接后一分钟自动禁止功能.
 * */

#include <stdio.h>
#include <glib.h>
#include <gio/gio.h>
#include <glib-object.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <syslog.h>

#define PERM_INIT			1
#define PERM_KEY_ON			0b101101
#define PERM_KEY_OFF		0b101100

GVolumeMonitor *monitor = NULL;
int permission_code = 1;
int timeout = 60;


void cb_list_remove_all_rdisk(gpointer data, gpointer user_data)
{
	GDrive *drive = data;

	syslog(LOG_INFO, "found device: %s\n", g_drive_get_name(drive));

	if (g_drive_can_stop(drive)) {
		g_drive_stop(drive,
				G_MOUNT_UNMOUNT_FORCE, 
				NULL, NULL,
				NULL,NULL);
		syslog(LOG_INFO, "stoped !\n");
	}
	if (g_drive_has_volumes(drive)) {
		if (g_drive_can_eject(drive))  {
			g_drive_eject_with_operation(drive,
					G_MOUNT_UNMOUNT_FORCE, 
					NULL, NULL,
					NULL, NULL);
			syslog(LOG_INFO, "ejected !\n");
		}
	}
}

void remvoe_all_rdisk()
{
	/* remove all the udisk */
	GList *list = NULL;
	list = g_volume_monitor_get_connected_drives(monitor);
	g_list_foreach(list, cb_list_remove_all_rdisk, NULL);
	g_list_free(list);
}


static int permission_is_ok()
{
	if (permission_code == PERM_KEY_ON) {
		return 1;
	} else {
		return 0;
	}
}

static void cb_drive_connected(GVolumeMonitor *monitor,
		GDrive *drive,
		gpointer user_data)
{

	if (permission_is_ok()) {
		syslog(LOG_INFO, "drive %s connected !\n", g_drive_get_name(drive));	
		return;
	}

	if (g_drive_can_stop(drive)) {
		syslog(LOG_INFO, "%s stoped !", g_drive_get_name(drive));
		g_drive_stop(drive,
				G_MOUNT_UNMOUNT_FORCE, 
				NULL, NULL,
				NULL,NULL);
	}
	
	return;
}

static void cb_volume_changed(GVolumeMonitor *monitor,
		GVolume *volume,
		gpointer user_data)
{
	GDrive *drive = NULL;
	
	if (permission_is_ok()) {
		syslog(LOG_INFO, "volume %s connected !\n", g_volume_get_name(volume));
		return;
	}

	drive = g_volume_get_drive(volume);
	if (NULL == drive) {
		if (g_volume_can_eject(volume)) {
			syslog(LOG_INFO, "volume %s ejected !\n", g_volume_get_name(volume));
			g_volume_eject_with_operation(volume,
					G_MOUNT_UNMOUNT_FORCE, 
					NULL, NULL,
					NULL, NULL);
			
		}
	}else if (g_drive_can_eject(drive)) {
		syslog(LOG_INFO, "drive %s ejected !\n", g_drive_get_name(drive));
		g_drive_eject_with_operation(drive,
				G_MOUNT_UNMOUNT_FORCE, 
				NULL, NULL,
				NULL, NULL);
	}
}

static void callback_timeout(int sig)
{
	permission_code = PERM_INIT;
	alarm(timeout);
	syslog(LOG_INFO, "permission is DISabled\n");
}

static void callback_unix_signal(int snu)
{
	if (snu == SIGRTMIN+0) {
		permission_code = PERM_KEY_OFF;
		remvoe_all_rdisk();
		syslog(LOG_INFO, "permission is DISabled !\n");
	} else if (snu == SIGRTMIN+1) {
		permission_code = PERM_KEY_ON;
		syslog(LOG_INFO, "permission is ENabled !\n");
	}
}

int set_user_env(void)
{
	FILE *fp = NULL;
	char buff[64];
	struct {
		char dbus_addr[256];
		int uid;
	}info;

	const char *cmd = "SESSIONPID=`ps -ef | grep xfce4-session | sed -n '1p' | awk '{print $2}'`;\
					   grep -z \"DBUS_SESSION_BUS_ADDRESS\" /proc/${SESSIONPID}/environ | cut -d= -f2-3";

	if (NULL == (fp = popen(cmd, "r")))
		return -10;
	if (NULL == fgets(info.dbus_addr, 256, fp))
		return -11;
	pclose(fp);

	cmd = "ps axo uid,cmd | grep xfce4-session | sed -n '1p' | awk '{print $1}'";
	if (NULL == (fp = popen(cmd, "r")))
		return -20;
	if (NULL == fgets(buff, 64, fp))
		return -21;
	info.uid = atoi(buff);
	pclose(fp);
	
	if (! g_setenv("DBUS_SESSION_BUS_ADDRESS", info.dbus_addr,1)) {
		return -1;
	}
	if (-1 == seteuid(info.uid)) {
		return -1;
	}

	return 0;
}

int main(int argc, const char **argv)
{
	GMainLoop *mainloop = NULL;
	gchar **env = NULL;

//	set_user_env();
	signal(SIGRTMIN+0, callback_unix_signal);
	signal(SIGRTMIN+1, callback_unix_signal);
//	signal(SIGALRM, callback_timeout);

	openlog(NULL, LOG_PID, LOG_SYSLOG);

	monitor = g_volume_monitor_get();
	
	remvoe_all_rdisk();


#if 0
	if (0 == g_signal_connect(monitor, "drive-connected", 
			G_CALLBACK (cb_drive_connected), "drive")) {
		syslog(LOG_ERR, "can`t connect the 'drive-connected'signal.\n");
		return -1;
	}
#endif

	if (0 == g_signal_connect(monitor, "volume-changed", 
			G_CALLBACK (cb_volume_changed), "volume")) {
		syslog(LOG_ERR, "can`t connect the 'volume-changed' signal.\n");
		return -1;
	}

	mainloop = g_main_loop_new(NULL, TRUE);
	g_main_loop_run(mainloop);

	g_object_unref(mainloop);

	return 0;
}
