/*
 * Override calls to getpwuid for getting the users homedir.
 * We need it to treat $SNAP_USER_COMMON as the homedir to
 * handle .minecraft and .lunarclient dirs.
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <pwd.h>
#include <string.h>
#include <dlfcn.h>

struct passwd *getpwuid(uid_t uid) {
    // Call the original getpwuid function
    struct passwd *(*original_getpwuid)(uid_t) = dlsym(RTLD_NEXT, "getpwuid");
    struct passwd *pw = original_getpwuid(uid);

    // Check if the environment variable SNAP_USER_COMMON is set
    char *snap_user_common = getenv("SNAP_USER_COMMON");

    if (pw && snap_user_common) {
        // Allocate memory for the new home directory
        char *new_home = malloc(strlen(snap_user_common) + 1);
        strcpy(new_home, snap_user_common);
        pw->pw_dir = new_home;
    }
    return pw;
}
