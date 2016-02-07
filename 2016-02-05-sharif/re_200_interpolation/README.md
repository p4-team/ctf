## Interpolation (Reverse, 200p)

    NEWTON is an autonomous unmanned aerial vehicle (UAV). Where the UAV is refueled at t=180 ?

    Path planning:
    t x y
    0; 35.645592; 50.951123;
    20; 35.144068; 50.467725;
    40; 34.729775; 48.204541;
    60; 34.204433; 46.117139;
    80; 33.602623; 44.908643;
    100; 33.162285; 42.337842;
    120; 33.712359; 40.140576;
    140; 33.931410; 38.580518;
    150; 33.894940; 37.745557;
    170; 33.474422; 36.273389;
    190; 35.32583531; 35.663648;
    210; 33.130089; 35.19047214;
    220; 32.409544; 35.141797;
    230; 32.085525; 34.786115;
    The flag is: [the bridge`s name near the refule place][Latitude of the place with 5 digits after the decimal point][Longitude of the place with 5 digits after the decimal point]

###ENG
[PL](#pl-version)

Task description mentions NEWTON and the title was "interpolation" - so we used Newton's interpolation method
to find `(x, y)` at `t=180`. This gave us location - after checking it in Google Maps, there was indeed a bridge nearby.

###PL version

Ponieważ zadanie wspominało o Newtonie i interpolacji, użyliśmy metody Newtona do znalezienia `(x, y)` w momencie
`t=180`. To dało nam współrzędne geograficzne - po sprawdzeniu ich na mapach Google, okazało się, że faktycznie jest
w pobliżu most, o który nas proszą w zadaniu.
