struct timeval{
	long long tv_sec;
	int tv_usec;
};
struct timezone{};
int gettimeofday(struct timeval *tv, struct timezone *tz){
	static int x=0;
	static int y=0;
	tv->tv_sec=x++;
	tv->tv_usec=y++;
	return 0;
}
