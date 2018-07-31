# kid vm (pwn 188p, 22 solved)

> Writing a vm is the best way to teach kids to learn vm escape.

## Analysis

### Wrap-around vulnerability in the guest memory allocator

When allocating guest memory, the subroutine 006F fails to check if the new request fits into available free space.

The only check implemented is 008F, that validates pre-existing usage:
```
006F alloc_memory    proc near
006F                 push    ax
0070                 push    bx
0071                 push    cx
0072                 push    dx
0073                 push    si
0074                 push    di
0075                 mov     ax, offset aSize ; "Size:"
0078                 mov     bx, 5
007B                 call    write_bytes
007E                 mov     ax, offset requested_size
0081                 mov     bx, 2
0084                 call    read_bytes
0087                 mov     ax, ds:requested_size
008A                 cmp     ax, 1000h
008D                 ja      short error_too_big
008F                 mov     cx, ds:free_space_offset
0093                 cmp     cx, 0B000h      ; heap size
0097                 ja      short error_guest_memory_is_full
0099                 mov     si, word ptr ds:allocated_count
009D                 cmp     si, 10h
00A0                 jnb     short error_too_many_memory
00A2                 mov     di, cx
00A4                 add     cx, 5000h       ; heap start
00A8                 add     si, si
00AA                 mov     ds:allocated_chunks[si], cx
00AE                 mov     ds:allocated_sizes[si], ax
00B2                 add     di, ax
00B4                 mov     ds:free_space_offset, di
00B8                 mov     al, ds:allocated_count
00BB                 inc     al
00BD                 mov     ds:allocated_count, al
00C0                 jmp     short restore_registers
00C2 ; ---------------------------------------------------------------------------
00C2
00C2 error_too_big:
00C2                 mov     ax, offset aTooBig ; "Too big\n"
00C5                 mov     bx, 8
00C8                 call    write_bytes
00CB                 jmp     short restore_registers
00CD ; ---------------------------------------------------------------------------
00CD
00CD error_guest_memory_is_full:
00CD                 mov     ax, offset aGuestMemoryIsFullPl ; "Guest memory is full! Please use the ho"...
00D0                 mov     bx, 32h
00D3                 call    write_bytes
00D6                 jmp     short restore_registers
00D8 ; ---------------------------------------------------------------------------
00D8
00D8 error_too_many_memory:
00D8                 mov     ax, offset aTooManyMemory ; "Too many memory\n"
00DB                 mov     bx, 10h
00DE                 call    write_bytes
00E1
00E1 restore_registers:
00E1                 pop     di
00E2                 pop     si
00E3                 pop     dx
00E4                 pop     cx
00E5                 pop     bx
00E6                 pop     ax
00E7                 retn
00E7 alloc_memory    endp
```

This can be exploited by performing 11 allocations of 0x1000 bytes each.
At that point next allocation is at 0x5000 + 11 * 0x1000 = 0x10000, wrapping to 0 as guest operates on 16-bit registers.
This allows for overwrite of guest code.

### Use-After-Free vulnerability in the host memory allocator

When deallocating host memory, the subroutine 0000000000000C8C includes option to skip `allocated_chunks` cleanup:
```
void __fastcall free_host_memory(__int16 mode, unsigned __int16 chunk_index)
{
  if ( chunk_index <= 0x10u )
  {
    switch ( mode )
    {
      case 2:
        free(allocated_chunks[(unsigned __int64)chunk_index]);
        allocated_chunks[(unsigned __int64)chunk_index] = 0LL;
        --g_alloc_count;
        break;
      case 3:
        free(allocated_chunks[(unsigned __int64)chunk_index]);
        allocated_chunks[(unsigned __int64)chunk_index] = 0LL;
        allocated_sizes[(unsigned __int64)chunk_index] = 0;
        --g_alloc_count;
        break;
      case 1:
        free(allocated_chunks[(unsigned __int64)chunk_index]);
        break;
    }
  }
  else
  {
    perror("Index out of bound!");
  }
}
```

This option is not reachable using original guest code.
However given previous vulnerability, we can control it using following `vmcall`:
```
ax = 0x0101
bx = mode
cx = chunk_index
```

## Exploitation

1. Modify code executing in guest by exploiting wrap-around vulnerability in the guest memory allocator

   The purpose is to expose host vulnerabilities via specific combinations of `vmcall` parameters, that are not reachable using original guest code.

2. Leak the address of host `libc` by exploiting use-after-free vulnerability in the host memory allocator

3. Increase `global_fast_max` by exploiting use-after-free vulnerability in the host memory allocator to corrupt the unsorted bin freelist

   The purpose is to enable fastbin for the next step.

4. Allocate memory overlapping with `_IO_2_1_stdout_.vtable` by exploiting use-after-free vulnerability in the host memory allocator to corrupt the fastbin freelist

5. Overwrite `_IO_2_1_stdout_.vtable` to use new table referring `one gadget RCE`

   The referred gadget is called immediately on next `putchar`.

Full exploit is attached [here](exploit.py).
