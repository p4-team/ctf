#ifndef XSIM
#define XSIM
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string>
#include <cstring>
#include <unistd.h>
#include <vector>
#define XK_MISCELLANY
#define XK_LATIN2
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XTest.h>

struct Color
{
    unsigned char r, g, b;
};

class XSim
{
    public:
    XSim();
    ~XSim();
    void getScreenshot();
    void getScreenshotRegion(int x, int y, int w, int h);
    void getPixel(int x, int y, Color* color);
    void queryCoords(int *x, int *y);
    void moveMouseTo(int x, int y);
    void click();
    void typeChar(wchar_t c);
    void pressK(int c);
    void releaseK(int c);
    void typeString(const wchar_t* str);
    void sleepW(int microseconds);
    int error();

    //private:
    XImage* image = NULL;
    Display* display = NULL;
    int errorFlag = 0;

};
#endif

