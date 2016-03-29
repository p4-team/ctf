#include <iostream>
#include <deque>
#include <sstream>
#include <iomanip>
#include <cmath>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XTest.h>
#include "xsim.h"
using namespace std;

const int keys[] = {XK_Down, XK_Up, XK_Left, XK_Right};
string lines[36];
int odw[500][500];
deque<int> sol;

int ny[] = {0, 0, -1, 1};
int nx[] = {1, -1, 0, 0};

int tx = 24, ty = 47;

int solve(int x, int y)
{
    odw[x][y] = 1;

    for(int i = 0; i < 4; ++i)
    {
        int cx = x+nx[i];
        int cy = y+ny[i];
        if(cx < 0 || cy < 0) continue;
        if(odw[cx][cy]) continue;
        if(cx == tx && cy == ty)
            return 1;
        if(lines[cx][cy] != ' ' && lines[cx][cy] != 'x') continue;
        if(solve(cx, cy) == 1)
        {
            sol.push_front(i);
            return 1;
        }
    }
    return 0;
}

vector<string> rown;

int main()
{
    XSim* xsim = new XSim();
    for(int j = 0; j < 3; ++j)
    {
        for(int i = 0; i < 500; ++i)
            for(int ii = 0; ii < 500; ++ii)
                odw[i][ii] = 0;
        sol.clear();

        for(int i = 0; i < 29; ++i)
        {
            getline(cin, lines[i]);
            if(lines[i] == "")
                --i;
        }
        for(int i = 26; i < 29; ++i)
        {
            string input = lines[i];
            stringstream stream(input);
            int a, b, c;
            char p;
            stream >> a;
            stream >> p;
            stream >> p;
            stream >> b;
            stream >> p;
            stream >> c;
            int delta = b*b-4*a*c;
            if(delta < 0)
            {
                rown.push_back("nrr");
            }
            else if(delta == 0)
            {
                double x = (-b)/(2.0*a);
                stringstream str;
                str << "x1=x2=" << fixed << setprecision(1) << x;
                rown.push_back(str.str());
            }
            else
            {
                double x1= (-b+sqrt(delta))/(2.0*a);
                double x2 = (-b-sqrt(delta))/(2.0*a);
                stringstream str;
                str << "x1=" << fixed << setprecision(1) << x1 << ";x2=" << fixed << setprecision(1) << x2;
                rown.push_back(str.str());
            }
        }
        cout << "ok, ok!" << endl;
        solve(1, 2);
        cout << "solved! now, go go!" << endl;
        xsim->sleepW(2000000);

        for(int i = 0; i < sol.size(); ++i)
        {
            xsim->pressK(keys[sol[i]]);
            xsim->releaseK(keys[sol[i]]);
        }
        xsim->pressK(XK_Down);
        xsim->releaseK(XK_Down);
        if(j < 2)
        {
            xsim->pressK(XK_Right);
            xsim->releaseK(XK_Right);
        }
    }

    for(int i = 0; i < rown.size()-1; ++i)
        cout << rown[i] << ",";
    cout << rown[rown.size()-1] << endl;
    char c;
    while(1)
        cin >> c;
    return 0;
}

