#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include <iostream>
#include <iomanip>

typedef int32_t int32;
typedef int64_t int64;

const void *last_accessed_pointer;

//#define ENABLE_VO_DEBUG_MESSAGES
void debug (const char *msg1, const char *msg2 = 0);
void debug (const char *msg1, const int arg2);
void debugptr (const char *ptr);

int end_of_execution (const char *&ptr);
int printf_command (const char *&ptr);
int strcmp_command (const char *&ptr);
void assign_variable_command (const char *&ptr);
void jump_command (const char *&ptr);
void if_then_else_command (const char *&ptr);
bool do_comparison (const char *&ptr);
int64 get_argument (const char *&ptr);
void skip_argument (const char *&ptr);

const int pointer_size = 8;
const int constant_size = 4;

const char *init_program (int *argcptr, char *argv[]);
int main_loop (const char *ptr);

int main (int argc, char *argv[]) {
  const char *ptr = init_program (&argc, argv);
  int ret = 0;
  try {
      ret = main_loop (ptr);
  } catch (const char *err_msg) {
      printf ("Exception: %s\n", err_msg);
  }
  return ret;
}

void debug (const char *msg1, const char *msg2) {
#ifdef ENABLE_VO_DEBUG_MESSAGES
    if (msg2 == 0) {
        printf ("\t--- %s\n", msg1);
    } else {
        printf ("\t--- %s | %s\n", msg1, msg2);
    }
#endif
}

void debug (const char *msg1, const int arg2) {
#ifdef ENABLE_VO_DEBUG_MESSAGES
  printf ("\t--- %s [0x%x]\n", msg1, arg2);
#endif
}

void debugptr (const char *ptr) {
#ifdef ENABLE_VO_DEBUG_MESSAGES
  printf ("\t\t[ptr-1, ptr, ptr+1] => [0x%x 0x%x 0x%x]\n", *(ptr-1), *ptr, *(ptr+1));
#endif
}

int main_loop (const char *ptr) {
  ptr += 8;
  for (;;) {
    debug("before switch-case...");
    debugptr (ptr);
    switch (*ptr++) {
      case 0x00:
        debug("0x00 -> end_of_execution");
        return end_of_execution (ptr);
      case 0x01:
        debug("0x01 -> if_then_else_command");
        debugptr (ptr);
        if_then_else_command (ptr);
        break;
      case 0x03:
        debug("0x03 -> jump_command");
        jump_command (ptr);
        break;
      case 0x05:
        debug("0x05 -> assign_variable_command");
        assign_variable_command (ptr);
        break;
      case 0x0F:
        debug("0x02 -> printf_command");
        printf_command (ptr);
        break;
      case 0x10:
        debug("0x04 -> strcmp_command");
        strcmp_command (ptr);
        break;
    }
  }
}

int end_of_execution (const char *&ptr) {
  const int arg0 = get_argument (ptr);
  return arg0;
}

int printf_command (const char *&ptr) {
  const char *format = (const char *) get_argument (ptr);
  return printf (format);
}

int strcmp_command (const char *&ptr) {
  const char *arg0 = (const char *) get_argument (ptr);
  const char *arg1 = (const char *) get_argument (ptr);
  debug("strcmp args:");
  debug("\t", arg0);
  debug("\t", arg1);
  return strcmp (arg0, arg1);
}

void assign_variable_command (const char *&ptr) {
  const int64 dest_ptr = get_argument (ptr);
  const int64 content = get_argument (ptr);
  last_accessed_pointer = (void *) dest_ptr;
  const char type = *ptr;
  ++ptr;
  if (type == 0x01) { // char dest
    *((char *) last_accessed_pointer) = char (content);
  } else if (type == 0x02) { // int dest
    *((int32 *) last_accessed_pointer) = int32 (content);
  } else if (type == 0x03) { // pointer dest
    *((int64 *) last_accessed_pointer) = content;
  } else {
    throw "assign_variable_command: wrong type";
  }
}

void jump_command (const char *&ptr) {
  const int offset = get_argument (ptr);
  ptr += offset;
}

void if_then_else_command (const char *&ptr) {
  const bool res = get_argument (ptr);
  const int thenpart = get_argument (ptr);
  const int elsepart = get_argument (ptr);
  if (res) {
    ptr += thenpart;
  } else {
    ptr += elsepart;
  }
}

bool do_comparison (const char *&ptr) {
  const char type = *ptr;
  ++ptr;
  if (type == 0x1) {
    debug ("do_comparison: 0x1 <");
    debugptr (ptr);
    const int64 arg0 = get_argument (ptr);
    const int64 arg1 = get_argument (ptr);
    return arg0 < arg1;
  } else if (type == 0x02) {
    debug ("do_comparison: 0x2 <=");
    const int64 arg0 = get_argument (ptr);
    const int64 arg1 = get_argument (ptr);
    return arg0 <= arg1;
  } else if (type == 0x03) {
    debug ("do_comparison: 0x3 >");
    const int64 arg0 = get_argument (ptr);
    const int64 arg1 = get_argument (ptr);
    return arg0 > arg1;
  } else if (type == 0x04) {
    debug ("do_comparison: 0x4 >=");
    const int64 arg0 = get_argument (ptr);
    const int64 arg1 = get_argument (ptr);
    return arg0 >= arg1;
  } else if (type == 0x05) {
    debug ("do_comparison: 0x5 ==");
    const int64 arg0 = get_argument (ptr);
    const int64 arg1 = get_argument (ptr);
    return arg0 == arg1;
  } else if (type == 0x06) {
    debug ("do_comparison: 0x6 !=");
    const int64 arg0 = get_argument (ptr);
    const int64 arg1 = get_argument (ptr);
    return arg0 != arg1;
  } else if (type == 0x07) {
    debug ("do_comparison: 0x7 &&");
    const int64 arg0 = get_argument (ptr);
    if (!arg0) {
      skip_argument (ptr);
      return false;
    }
    const int64 arg1 = get_argument (ptr);
    return bool(arg1);
  } else if (type == 0x08) {
    debug ("do_comparison: 0x8 ||");
    const int64 arg0 = get_argument (ptr);
    if (arg0) {
      skip_argument (ptr);
      return true;
    }
    const int64 arg1 = get_argument (ptr);
    return bool(arg1);
  } else {
    throw "wrong operator";
  }
}

int64 get_argument (const char *&ptr) {
  const char type = *ptr;
  ++ptr;
  if (type == 0x01) {
    debug ("get_argument: 0x01 -> pointer argument");
    const int **arg0 = (const int **) ptr;
    ptr += pointer_size;
    last_accessed_pointer = *arg0;
    return **arg0;
  } else if (type == 0x02) {
    debug ("get_argument: 0x02 -> constant argument");
    const int32 *arg0 = (const int32 *) ptr;
    ptr += constant_size;
    last_accessed_pointer = 0;
    return *arg0;
  } else if (type == 0x03) {
    debug ("get_argument: 0x03 -> pointer to char argument");
    const char **arg0 = (const char **) ptr;
    ptr += pointer_size;
    last_accessed_pointer = *arg0;
    return **arg0;
  } else if (type == 0x04) { 
    debug ("get_argument: 0x04 -> pointer to pointer argument");
    const int64 **arg0 = (const int64 **) ptr;
    ptr += pointer_size;
    last_accessed_pointer = *arg0;
    return **arg0;
  } else if (type == 0x05) {
    debug ("get_argument: 0x05 -> minus operator");
    const int64 res = -get_argument (ptr);
    last_accessed_pointer = 0;
    return res;
  } else if (type == 0x06) {
    debug ("get_argument: 0x06 -> boolean condition: 1< 2<= 3> 4>= 5== 6!= 7&& 8||");
    debugptr (ptr);
    const bool res = do_comparison (ptr);
    last_accessed_pointer = 0;
    return res;
  } else if (type == 0x07) {
    debug ("get_argument: 0x07 -> char variable reference");
    const int32 *offset = (const int32 *) ptr;
    ptr += constant_size;
    last_accessed_pointer = ptr + (*offset);
    const char *var = (const char *) last_accessed_pointer;
    return *var;
  } else if (type == 0x08) {
    debug ("get_argument: 0x08 -> int variable reference");
    const int32 *offset = (const int32 *) ptr;
    ptr += constant_size;
    last_accessed_pointer = ptr + (*offset);
    const int32 *var = (const int32 *) last_accessed_pointer;
    return *var;
  } else if (type == 0x09) {
    debug ("get_argument: 0x09 -> pointer variable reference");
    const int32 *offset = (const int32 *) ptr;
    ptr += constant_size;
    last_accessed_pointer = ptr + (*offset);
    const int64 *var = (const int64 *) last_accessed_pointer;
    return *var;
  } else if (type == 0x0A) {
    debug ("get_argument: 0x0A -> char array dereference");
    const int64 base_ptr = get_argument (ptr);
    const int32 array_index = get_argument (ptr);
    const char &val = ((const char *) base_ptr)[array_index];
    last_accessed_pointer = &val;
    return val;
  } else if (type == 0x0B) {
    debug ("get_argument: 0x0B -> int array dereference");
    const int64 base_ptr = get_argument (ptr);
    const int32 array_index = get_argument (ptr);
    const int32 &val = ((const int32 *) base_ptr)[array_index];
    last_accessed_pointer = &val;
    return val;
  } else if (type == 0x0C) {
    debug ("get_argument: 0x0C -> pointer array dereference");
    const int64 base_ptr = get_argument (ptr);
    const int32 array_index = get_argument (ptr);
    const void *&val = ((const void **) base_ptr)[array_index];
    last_accessed_pointer = &val;
    return int64 (val);
  } else if (type == 0x0D) {
    debug ("get_argument: 0x0D -> address-of accessed lhs argument");
    /*const int64 accessed_value =*/ get_argument (ptr);
    if (last_accessed_pointer == 0) {
      throw "accessed argument is rhs and has no address";
    }
    const int64 res = int64 (last_accessed_pointer);
    last_accessed_pointer = 0;
    return res;
  } else if (type == 0x0E) {
    debug ("get_argument: 0x0E -> subtract");
    const int64 left = get_argument (ptr);
    const int64 right = get_argument (ptr);
    last_accessed_pointer = 0;
    return left - right;
  } else if (type == 0x0F) {
    debug ("get_argument: 0x0F -> printf call");
    last_accessed_pointer = 0;
    return printf_command (ptr);
  } else if (type == 0x10) {
    debug ("get_argument: 0x10 -> strcmp call");
    last_accessed_pointer = 0;
    return strcmp_command (ptr);
  } else if (type == 0x11) {
    debug ("get_argument: 0x11 -> string constant");
    const char **str = (const char **) ptr;
    ptr += pointer_size;
    last_accessed_pointer = str;
    return int64 (*str);
  } else if (type == 0x12) {
    debug ("get_argument: 0x12 -> add");
    const int64 left = get_argument (ptr);
    const int64 right = get_argument (ptr);
    last_accessed_pointer = 0;
    return left + right;
  } else {
    debug ("get_argument: unknown-type", type);
    throw "wrong type";
  }
}

void skip_argument (const char *&ptr) {
  const char type = *ptr;
  ++ptr;
  switch (type) {
    case 0x01:
    case 0x03:
    case 0x04:
    case 0x11:
      ptr += pointer_size;
      break;
    case 0x02:
    case 0x07:
    case 0x08:
    case 0x09:
      ptr += constant_size;
      break;
    case 0x06:
      ++ptr;
    case 0x0A:
    case 0x0B:
    case 0x0C:
    case 0x0E:
    case 0x10:
    case 0x12:
      skip_argument (ptr);
    case 0x0D:
    case 0x05:
    case 0x0F:
      skip_argument (ptr);
      break;
    default:
      throw "wrong type";
  }
}

