# Patience (RE, 769p)

This was a haskell reversing challenge. If this doesn't fill you with dread, this means that probably either:

- you are most 1338 pr0 xakep r3v3rse engineer ever living
- you don't know what you're going to see.

Either way, you're going to have some serious fun. In fact, I've never seen anyone actually reverse engineer (non-trivial) haskell binary before - most challenges are actually cracked with black-box solutions or other side channels. This task is no different - we are given .cmm file along with compiled binary.

CMM files are dump of late-stage intermediate language from GHC. This is going to make our life way easier - we don't have to reverse haskell thunks, we have everything in plain text... well, sort of.

## How to be lazy

A word of introduction to the beautiful world of functional programming. Haskell is a lazy language. But not just your average slightly-procrastinating kind - everything is delayed as long as it possibly can be, and I mean it. For example, consider this function:

```haskell
integers n = n : integers (n+1)
```

if you don't speak Haskell, this is conceptually equivalent to following python code:

```python
def integers(n):
    return [n] + integers(n + 1)
```

Do you see anything wrong with this code? Exactly, this is not a terribly useful function - it'll recurse forever, or rather eat all your available stack space and explode. Not in Haskell though - you can take first 100 elements of that list, and everything will work, because haskell is *lazy* - only necessary elements will be evaulated.

But this still doesn't explain just how lazy Haskell is. Consider this:

```haskell
foo (2 + 2)
```

This is just invoaction of function `foo` with parameter `4`. Wait, wrong, I lied to you. The parameter is `2 + 2`, and it's not actually evaluated until it's needed. Hell, you could've passed `1 / 0` and nothing bad would happen, at least until something actually evaulates the parameter.

## Reversing

So, why the introduction? Well, this is how `main` function looks like in dump:

```
==================== Output Cmm ====================
[section ""data" . :Main.main_closure" {
     :Main.main_closure:
         const :Main.main_info;
         const 0;
         const 0;
         const 0;
 },
 :Main.main_entry() //  [R1]
         { info_tbl: [(c3bb,
                       label: :Main.main_info
                       rep:HeapRep static { Thunk })]
           stack_info: arg_space: 8 updfr_space: Just 8
         }
     {offset
       c3bb:
           _01D::P64 = R1;
           if ((Sp + 8) - 24 < SpLim) goto c3bc; else goto c3bd;
       c3bc:
           R1 = _01D::P64;
           call (stg_gc_enter_1)(R1) args: 8, res: 0, upd: 8;
       c3bd:
           (_c3b8::I64) = call "ccall" arg hints:  [PtrHint,
                                                    PtrHint]  result hints:  [PtrHint] newCAF(BaseReg, _01D::P64);
           if (_c3b8::I64 == 0) goto c3ba; else goto c3b9;
       c3ba:
           call (I64[_01D::P64])() args: 8, res: 0, upd: 8;
       c3b9:
           I64[Sp - 16] = stg_bh_upd_frame_info;
           I64[Sp - 8] = _c3b8::I64;
           R2 = Main.main_closure;
           R1 = GHC.TopHandler.runMainIO_closure;
           Sp = Sp - 16;
           call stg_ap_p_fast(R2, R1) args: 24, res: 0, upd: 24;
     }
 }]
```

Beautiful, isn't it? What's going on here? Nothing, actually. All this code does is:

```haskell
runMainIO (main_closure)
```

where `main_closure` is well, closure from main (bound function, a common occurence in functional programming).

Let's dig deeper - what's inside this `main_closure`?

```haskell
Main.main_entry() //  [R1]
        { info_tbl: [(c3aW,
                      label: Main.main_info
                      rep:HeapRep static { Thunk })]
          stack_info: arg_space: 8 updfr_space: Just 8
        }
    {offset
      c3aW:
          _rFG::P64 = R1;
          if ((Sp + 8) - 24 < SpLim) goto c3aX; else goto c3aY;
      c3aX:
          R1 = _rFG::P64;
          call (stg_gc_enter_1)(R1) args: 8, res: 0, upd: 8;
      c3aY:
          (_c3aT::I64) = call "ccall" arg hints:  [PtrHint,
                                                   PtrHint]  result hints:  [PtrHint] newCAF(BaseReg, _rFG::P64);
          if (_c3aT::I64 == 0) goto c3aV; else goto c3aU;
      c3aV:
          call (I64[_rFG::P64])() args: 8, res: 0, upd: 8;
      c3aU:
          I64[Sp - 16] = stg_bh_upd_frame_info;
          I64[Sp - 8] = _c3aT::I64;
          R5 = sat_s2Rj_closure+1;
          R4 = sat_s2Rf_closure;
          R3 = GHC.Base.$fMonadIO_closure;
          R2 = Data.Foldable.$fFoldable[]_closure;
          R1 = Data.Foldable.forM__closure;
          Sp = Sp - 16;
          call stg_ap_pppp_fast(R5,
                                R4,
                                R3,
                                R2,
                                R1) args: 24, res: 0, upd: 24;
    }                                               
}                                                   
```

Again, a lot of code. And again, This is equivalent to:

```haskell
forM (s2Rj_closure) (s2Rf_closure)
```

So, invocation of single function with two closures.

And again...

```haskell
==================== Cmm produced by new codegen ====================
[section ""data" . sat_s2Rf_closure" {
     sat_s2Rf_closure:
         const sat_s2Rf_info;
         const 0;
         const 0;
         const 0;
 },
 sat_s2Rf_entry() //  [R1]
         { info_tbl: [(c3aH,
                       label: sat_s2Rf_info
                       rep:HeapRep static { Thunk })]
           stack_info: arg_space: 8 updfr_space: Just 8
         }
     {offset
       c3aH:
           _s2Rf::P64 = R1;
           goto c3aC;
       c3aC:
           if ((old + 0) - <highSp> < SpLim) goto c3aI; else goto c3aJ;
       c3aI:
           R1 = _s2Rf::P64;
           call (stg_gc_enter_1)(R1) args: 8, res: 0, upd: 8;
       c3aJ:
           (_c3aE::I64) = call "ccall" arg hints:  [PtrHint,
                                                    PtrHint]  result hints:  [PtrHint] newCAF(BaseReg, _s2Rf::P64);
           if (_c3aE::I64 == 0) goto c3aG; else goto c3aF;
       c3aG:
           call (I64[_s2Rf::P64])() args: 8, res: 0, upd: 8;
       c3aF:
           I64[(old + 24)] = stg_bh_upd_frame_info;
           I64[(old + 16)] = _c3aE::I64;
           R3 = Main.flags_closure+2;
           R2 = Main.idx'_closure+1;
           R1 = GHC.Base.map_closure;
           call stg_ap_pp_fast(R3, R2, R1) args: 24, res: 0, upd: 24;
     }
 }]
```

Which basically means (closure names by me):

```haskell
map (idx_closure) (flags_closure)
```

So again, single function invocation, with closure parameters, and a lot of junk.

I'll spare you the details - when you know what to expect (i.e. a LOT of thunks), reversing is quite straightforward (except you need a LOT of, well, *patience*).

This is the reversed code, which should be **very** similar to the original:

```haskell
module Main where

import Data.Bits
import Data.Char
import Control.Monad
import System.IO
import Data.Function.Memoize

s0 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'\"()*+,-./:;<=>?@[\\]^_`{|}~"
s1 = "1vI{e[8Td]-nQ.7O\"bl(jq@<0Vy&Z3~\\ps,aD^;BN9JUoh|CE2_6!G'rHuf>$S%MxgzKY4`c+WXA5F)mR}#PtL?*=i/:wk"
s2 = "Bp}i{XU%f$DR\\0<Lx=o\"Sl`bz)-e62|&JqFT!(C5yh;@u*.WaZ#Qv,?cr8wEm4_t19PH:j]>[NVMn7YGkK'^/~OIdsA+3g"
s3 = "_r+#yh[Y)S8aXJwV&jv\"o=I(6>pg,f-M]qbN4'EDKF\\t<3G%|$csPQm}~0@R;uU2z9iWB./HCk!{:Od^ZT7`Anl1e5L*x?"

data Index = Index Int Int

f :: Int -> [Char]
f 0 = s0
f arg = s1 ++ f (subtract 1 arg) ++ s2 ++ f (subtract 1 arg) ++ s3

idx :: Index -> Char
idx (Index i j) = (f i !! j)

flags = [Index 0 39,
     Index 5 282,
     Index 6 16240,
     Index 9 162889,
     Index 14 523151,
     Index 17 5536393,
     Index 7616 133142712,
     Index 8799 122076774,
     Index 8656 370998818,
     Index 9835 12169334,
     Index 9023 316222630,
     Index 9402 20517998,
     Index 9509 206287754,
     Index 5656 439741488,
     Index 9020 254692819,
     Index 5337 505473338,
     Index 7860 66985734,
     Index 5342 343561367,
     Index 7797 237439774,
     Index 6145 303374550,
     Index 5842 469397741,
     Index 6262 125811292,
     Index 8861 285489743,
     Index 9917 203482576,
     Index 6210 65894981,
     Index 5807 160395306,
     Index 6950 411117612,
     Index 9261 130413308,
     Index 6224 532384558,
     Index 5304 107223978,
     Index 6533 292707045,
     Index 8303 284494291,
     Index 9948 119890013,
     Index 8254 430252526,
     Index 8249 142828351,
     Index 8799 452127715,
     Index 6071 491307991,
     Index 8803 154654024,
     Index 9328 181393976,
     Index 6253 103923077,
     Index 7886 450071326,
     Index 7721 342235485,
     Index 6802 429438438,
     Index 6391 504612462,
     Index 5300 23633538,
     Index 9418 315942207,
     Index 9873 228342978,
     Index 6361 510000394,
     Index 5816 485654100,
     Index 8533 347840847,
     Index 9931 517634651,
     Index 8209 122749414,
     Index 9873 484029647,
     Index 9346 273221045]

main = do
  forM_ (map idx flags) $ \i -> do
    putChar i
    hFlush stdout
```

Not a lot of code, for huge binary that it produced, eh?

The problem is simple - `idx` function is very slow. But we can make it faster. I was too *lazy* to rewrite everything to my usual language of choice (python), so I just implemented faster version of `idx` straight in haskell:

```haskell
fsize' :: Int -> Integer
fsize' 0 = fromIntegral $ length s0
fsize' i = 2 * fsize (i - 1) + 3 * fsize 0

fsize :: Int -> Integer
fsize = memoize fsize'

idx' :: Index -> Char
idx' (Index i j) =
    if i == 0 then s0 !! j
    else if fromIntegral j < fsize0 then s1 !! j
    else if fromIntegral j < fsize1 then idx' $ Index (i - 1) (j - fromInteger fsize0)
    else if fromIntegral j < fsize2 then s2 !! (j - fromInteger fsize1)
    else if fromIntegral j < fsize3 then idx' $ Index (i - 1) (j - fromInteger fsize2)
    else s3 !! (j - fromInteger fsize3)
    where fsize0 = fsize 0
          fsize1 = fsize0 + fsize (i - 1)
          fsize2 = fsize1 + fsize0
          fsize3 = fsize2 + fsize (i - 1)
```

And that's basically it - after running reversed version, correct flag is produced in seconds:

```
N1CTF{did_cmm_helped?1109ef6af4b2c6fc274ddc16ff8365d1}
```

PS. Yes, it did.
