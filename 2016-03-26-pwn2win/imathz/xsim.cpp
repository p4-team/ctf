
#include "xsim.h"

#define XYINDEX(x, y, img) \
    ((y) * img->bytes_per_line) + \
    (((x) + img->xoffset) / img->bitmap_unit) * (img->bitmap_unit >> 3)


XSim::XSim()
{
    display = XOpenDisplay(NULL);
    if (display == NULL)
    {
        fprintf (stderr, "Can't open display!\n");
        errorFlag = 1;
    }
}

XSim::~XSim()
{
    if(image != NULL)
        XFree(image);
    image = NULL;
}

void XSim::getScreenshot()
{
    if(image != NULL) XFree(image);
    image = XGetImage(display, DefaultRootWindow (display), 0, 0,
                      XDisplayWidth(display, DefaultScreen (display)),
                      XDisplayHeight(display, DefaultScreen (display)), AllPlanes, XYPixmap);
}

void XSim::getScreenshotRegion(int x, int y, int w, int h)
{
    if(image != NULL)
        XFree(image);
    image = XGetImage(display, DefaultRootWindow(display), x, y, w, h, AllPlanes, XYPixmap);
}

void XSim::getPixel(int x, int y, Color* color)
{
    if(image == NULL)
    {
        fprintf(stderr, "Error in taking screenshot!\n");
        errorFlag = 1;
        return;
    }
    //XColor c;
    //unsigned long pixel = XGetPixel(image, x, y);
    unsigned long pixel = 0, px;
    register char *src;
    register char *dst;
    register int i, j;
    int bits, nbytes;
    long plane = 0;
    nbytes = image->bitmap_unit >> 3;
    //printf("nbytes: %d depth: %d\n", nbytes, image->depth);
    int pos = XYINDEX(x, y, image);
    for (i = image->depth; --i >= 0; )
    {
        src = &image->data[pos + plane];
        dst = (char *)&px;
        px = 0;
        for (j = nbytes; --j >= 0; ) *dst++ = *src++;
        bits = (x + image->xoffset) % image->bitmap_unit;
        pixel = (pixel << 1) | (((((char *)&px)[bits>>3])>>(bits&7)) & 1);
        plane = plane + (image->bytes_per_line * image->height);
    }
    color->r = (pixel & image->red_mask) >> 16;
    color->g = (pixel & image->green_mask) >> 8;
    color->b = (pixel & image->blue_mask);
    //printf("%d %d %d", color->r, color->g, color->b);
}

void XSim::queryCoords(int* x, int* y)
{
    XEvent event;
    XQueryPointer (display, DefaultRootWindow (display),
                   &event.xbutton.root, &event.xbutton.window,
                   &event.xbutton.x_root, &event.xbutton.y_root,
                   &event.xbutton.x, &event.xbutton.y,
                   &event.xbutton.state);
    *x = event.xbutton.x;
    *y = event.xbutton.y;
}

void XSim::moveMouseTo(int x, int y)
{
    XTestFakeMotionEvent(display, 0, x, y, CurrentTime);
    XFlush(display);
    usleep(1);
}

void XSim::click()
{
    XTestFakeButtonEvent(display, 1, True, CurrentTime);
    //XFlush(display);
    //usleep(1);
    XTestFakeButtonEvent(display, 1, False, CurrentTime);
    XFlush(display);
    usleep(1);
}

void XSim::typeChar(wchar_t c)
{
    switch(c)
    {
    case L'ą':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_aogonek);
        releaseK(XK_aogonek);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ę':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_eogonek);
        releaseK(XK_eogonek);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ć':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_cacute);
        releaseK(XK_cacute);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ł':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_lstroke);
        releaseK(XK_lstroke);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ś':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_sacute);
        releaseK(XK_sacute);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ó':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_oacute);
        releaseK(XK_oacute);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ż':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_zabovedot);
        releaseK(XK_zabovedot);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ź':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_zacute);
        releaseK(XK_zacute);
        releaseK(XK_ISO_Level3_Shift);
        break;
    case L'ń':
        pressK(XK_ISO_Level3_Shift);
        pressK(XK_nacute);
        releaseK(XK_nacute);
        releaseK(XK_ISO_Level3_Shift);
        break;
    default:
        pressK(c);
        releaseK(c);
        break;
    }

}

void XSim::pressK(int c)
{
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, c), 1, CurrentTime);
    //XFlush(display);
    //usleep(1);
}

void XSim::releaseK(int c)
{
    XTestFakeKeyEvent(display, XKeysymToKeycode(display, c), 0, CurrentTime);
    XFlush(display);
    usleep(1);
}

void XSim::typeString(const wchar_t* str)
{
    int n = wcslen(str);
    for(int i = 0; i < n; ++i)
        typeChar(str[i]);
    XFlush(display);
    usleep(1);
}

void XSim::sleepW(int microseconds)
{
    usleep(microseconds);
}

int XSim::error()
{
    return errorFlag;
}

