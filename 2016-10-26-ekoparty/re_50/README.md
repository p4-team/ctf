# F#ck (re 50)


###ENG
[PL](#pl-version)

In the task we get a [binary](FlagGenerator.exe) which is written in F#.
Like every other .NET binary it can be nicely decompiled by ILSpy.

With this we didn't even need to reverse the algorithm at all.
We simply modified the decompiled code we got so that we could compile it again:

```csharp
using System;
using System.Globalization;
 
class X
{
	public string str;

	public int[] ccIndices;

	internal X(string str, int[] ccIndices)
	{
		this.str = str;
		this.ccIndices = ccIndices;
	}

	public string Invoke(int i)
	{
		if (i == this.ccIndices.Length - 1)
		{
			return this.str.Substring(i);
		}
		int num = this.ccIndices[i];
		return this.str.Substring(num, this.ccIndices[i + 1] - num);
	}
}
 
public class Test
{
	public static string get_flag(string str)
	{
		int[] array = StringInfo.ParseCombiningCharacters(str);
		int num = array.Length;
		X fSharpFunc = new X(str, array);
		string[] array2 = new string[num];
		int num2 = 0;
		int num3 = num - 1;
		if (num3 >= num2)
		{
			do
			{
				array2[num2] = fSharpFunc.Invoke(num2);
				num2++;
			}
			while (num2 != num3 + 1);
		}
		string[] array3 = array2;
		Array.Reverse(array3);
		return string.Join("", array3);
	}
 
	public static void Main()
	{
		Console.WriteLine(get_flag("t#hs_siht_kc#f"));
	}
}
```

And we got `EKO{f#ck_this_sh#t}`.

###PL version

W zadaniu dostajemy [program](FlagGenerator.exe) napisany w F#.
Jak każda inna binarka .NET można go ładnie zdekompilować za pomocą ILSpy.

Uzyskujemy w ten sposób dość ładny kod i nie było potrzeby nawet reversować algorytmu.
Zmodyfikowaliśmy uzyskany kod tak, żeby dało się go skompilować i uruchomić:


```csharp
using System;
using System.Globalization;
 
class X
{
	public string str;

	public int[] ccIndices;

	internal X(string str, int[] ccIndices)
	{
		this.str = str;
		this.ccIndices = ccIndices;
	}

	public string Invoke(int i)
	{
		if (i == this.ccIndices.Length - 1)
		{
			return this.str.Substring(i);
		}
		int num = this.ccIndices[i];
		return this.str.Substring(num, this.ccIndices[i + 1] - num);
	}
}
 
public class Test
{
	public static string get_flag(string str)
	{
		int[] array = StringInfo.ParseCombiningCharacters(str);
		int num = array.Length;
		X fSharpFunc = new X(str, array);
		string[] array2 = new string[num];
		int num2 = 0;
		int num3 = num - 1;
		if (num3 >= num2)
		{
			do
			{
				array2[num2] = fSharpFunc.Invoke(num2);
				num2++;
			}
			while (num2 != num3 + 1);
		}
		string[] array3 = array2;
		Array.Reverse(array3);
		return string.Join("", array3);
	}
 
	public static void Main()
	{
		Console.WriteLine(get_flag("t#hs_siht_kc#f"));
	}
}
```

I dostaliśmy: `EKO{f#ck_this_sh#t}`.
