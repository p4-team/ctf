# RrEeGgEeXx (re 75)

###ENG
[PL](#pl-version)

In the task we got a [binary](RegexAuth.exe) written in C#.
Again as with the F# binary in RE50, we can simply decompile the code with ILSpy.
Most of it is not important - the only important bit is flag verification:

```csharp
Program.check_regex("^.{40}$", input) 
&& Program.check_regex("\\w{3}\\{.*\\}", input) 
&& Program.check_regex("_s.*e_", input) 
&& Program.check_regex("\\{o{2}O{2}o{2}", input) 
&& Program.check_regex("O{2}o{2}O{2}\\}", input) 
&& Program.check_regex("sup3r_r3g3x_challenge", input)
```

It's quite clear that the flag has to match all expressions:

1. Flag has to have exactly 40 characters
2. Flag contains 3 random letters then `{` any number of random characters and `}` -> this is flag format so `EKO{xx}`
3. Flag has to contain `_s` then any number of random characters and then `e_`
4. Flag has to contain `{ooOOoo` -> we can combine this with flag start
5. Flag has to contain `OOooOO}` -> we can combine this with flag end
6. Flag has to contain `sup3r_r3g3x_challenge` -> we can combine this with 3.

This quite easily gives us: `EKO{ooOOoo_sup3r_r3g3x_challenge_OOooOO}`

###PL version

W zadaniu dostajemy [aplikacje](RegexAuth.exe) napisaną w C#.
Podobnie jak w zadaniu z F# RE50, możemy zdekompilować kod za pomocą ILSpy.
Większość kodu nie jest istotna - jedyny ważny fragment to weryfikacja flagi:

```csharp
Program.check_regex("^.{40}$", input) 
&& Program.check_regex("\\w{3}\\{.*\\}", input) 
&& Program.check_regex("_s.*e_", input) 
&& Program.check_regex("\\{o{2}O{2}o{2}", input) 
&& Program.check_regex("O{2}o{2}O{2}\\}", input) 
&& Program.check_regex("sup3r_r3g3x_challenge", input)
```

Jak nie trudno zauważyć flaga musi spełniać wszystkie parametry:

1. Flaga ma dokładnie 40 znaków
2. Flaga zawiera 3 losowe litery, następnie `{`, dowolną liczbę znaków i na koniec `}` -> to jest format flagi więc `EKO{xx}`
3. Flaga musi zawierać `_s` następnie dowolną liczbę znaków i potem `e_`
4. Flaga musi zawierać `{ooOOoo` -> możemy połączyć to z początkiem flagi
5. Flaga musi zawierać `OOooOO}` -> możemy połączyć to z końcem flagi
6. Flaga musi zawierać `sup3r_r3g3x_challenge` -> możemy połączyć to z 3

To dość prosto daje nam: `EKO{ooOOoo_sup3r_r3g3x_challenge_OOooOO}`
