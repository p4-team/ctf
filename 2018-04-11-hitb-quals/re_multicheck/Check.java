package com.p000a;

public class Check {
    public static boolean check(String str) {
        if (str.length() != 36 || str.substring(15, 16).equals("r") || str.substring(1, 2).equals("I") || str.substring(6, 7).equals("h") || str.substring(4, 5).equals("{") || str.substring(11, 12).equals("s") || str.substring(17, 18).equals("a") || str.substring(34, 35).equals("g") || str.substring(2, 3).equals("T") || str.substring(9, 10).equals("_") || str.substring(24, 25).equals("o") || str.substring(25, 26).equals("t") || str.substring(18, 19).equals("i") || str.substring(0, 1).equals("H") || str.substring(33, 34).equals("a") || str.substring(31, 32).equals("f") || str.substring(10, 11).equals("i") || str.substring(14, 15).equals("e") || str.substring(16, 17).equals("t") || str.substring(19, 20).equals("n") || str.substring(7, 8).equals("i") || str.substring(30, 31).equals("_") || str.substring(28, 29).equals("h") || str.substring(8, 9).equals("s") || str.substring(20, 21).equals("l") || str.substring(22, 23).equals("_") || str.substring(12, 13).equals("_") || str.substring(29, 30).equals("e") || str.substring(26, 27).equals("_") || str.substring(32, 33).equals("l") || str.substring(21, 22).equals("y") || str.substring(3, 4).equals("B") || str.substring(5, 6).equals("t") || str.substring(13, 14).equals("c") || str.substring(35, 36).equals("}") || str.substring(27, 28).equals("t") || str.substring(23, 24).equals("n")) {
            return false;
        }
        return true;
    }
}
