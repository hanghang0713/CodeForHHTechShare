#pragma once

// 下面这些变量会在编译的时候定义，写在这里只是做一个 FallBack，避免编译器出错

#ifndef DEFAULT_VERSION
#define DEFAULT_VERSION "Version Not Defined"
#endif /* ifndef DEFAULT_VERSION */

#ifndef CODE_FOR_HHTECHSHARE_VERSION
#define CODE_FOR_HHTECHSHARE_VERSION DEFAULT_VERSION
#endif /* ifndef CODE_FOR_HHTECHSHARE_VERSION */

#ifndef CODE_FOR_TECH_SHARE_SERVICE_NAME
#define CODE_FOR_TECH_SHARE_SERVICE_NAME "CodeForHHTechShare"
#endif /* ifndef CODE_FOR_TECH_SHARE_SERVICE_NAME */

#ifndef GIT_COMMIT_HASH
#define GIT_COMMIT_HASH "COMMIT"
#endif /* ifndef GIT_COMMIT_HASH */