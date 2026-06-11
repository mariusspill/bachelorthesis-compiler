#include <inttypes.h> // for int64_t typedefs
#include <stdbool.h>  // C-booleans are a typedef to int
#include <stdio.h>    // for debug printing
#include <stdlib.h>   // For malloc
#include <string.h>   // For memcpy

// –– I/O Operations –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

void print_int64(int64_t x) {
    printf("%" PRId64 "\n", x);
}

int64_t input_int64() {
    int64_t x;
    int c;

    do {
        if (scanf("%" SCNd64, &x) == 1) 
            break; 

        while ((c = getchar()) != '\n' && c != EOF);
    } while (1);

    return x;
}

// –– Garbage Collector: API –––––––––––––––––––––––––––––––––––––––––––––––––––

// first free word on from-space
int64_t* gc_free_ptr;       

// first word after from-space
int64_t* gc_fromspace_end;  

void gc_init(
  // stack pointer at begin of main
  int64_t* stack_begin,   
  // initial size of from-/to-space in 64bit-words
  uint64_t heap_size      
);

void gc_collect(
  // current stack pointer
  int64_t* stack_end,       
  // to reallocate from-/to-space, if collection didn't free enough space
  uint64_t requested_words
);

// DEBUG PRINTING
//
// Compiling with the DEBUG preprocessor symbol (passing -D DEBUG to
// gcc) makes the garbage collector print debug information while it
// is running.

// –– Garbage Collector: Implementation ––––––––––––––––––––––––––––––––––––––––

#ifdef DEBUG
  #define printf_if_debug(...) printf(__VA_ARGS__)
#else
  #define printf_if_debug(...)
#endif

void* malloc_safe(uint64_t num_bytes) {
  void* p = malloc(num_bytes);
  if (p == NULL) {
    printf("PANIC: Garbage collector ran out of memory.\n");
    exit(1);
  }
  return p;
}

int64_t* gc_fromspace_begin;

int64_t* gc_tospace_begin;
int64_t* gc_tospace_end;

int64_t* gc_stack_begin;

void gc_init(
  int64_t* stack_begin,   
  uint64_t heap_size      
) {
  printf_if_debug("\n–––––––––– gc_init ––––––––––\n");
  printf_if_debug("Initial space size in words: %" PRIu64 "\n", heap_size);

  gc_stack_begin = stack_begin;

  gc_fromspace_begin = malloc_safe(heap_size * 8);
  gc_fromspace_end = gc_fromspace_begin + heap_size;

  gc_tospace_begin = malloc_safe(heap_size * 8);
  gc_tospace_end = gc_tospace_begin + heap_size;

  gc_free_ptr = gc_fromspace_begin;
  printf_if_debug("––––––––––––––––––––––––––––––\n");
} 

bool gc_contains_heap_ptr(int64_t* p) {
  return *p & 1;
}

bool gc_is_forwarded(int64_t* p) {
  return *p & 1;
}

int64_t* gc_remove_ptr_tag(int64_t* p) {
  return (int64_t*) (((int8_t*) p) - 1);
}

int64_t* gc_add_ptr_tag(int64_t* p) {
  return (int64_t*) (((int8_t*) p) + 1);
}

// Copies an object to wherever free_ptr points to and increases free_ptr.
// Updates the pointer to the object to the new location.
void gc_copy_if_heap_ptr(int64_t* p) {
  /* printf_if_debug("  PTR: %" PRIu64 "\n", (uint64_t) p); */
  // Check if p points to a heap-pointer
  if (gc_contains_heap_ptr(p)) {
    // p is actually a pointer to a tagged heap pointer, e.g. a
    // pointer to a stack location that contains a tagged heap pointer.
    int64_t** object_ptr_ptr = (int64_t**) p;

    // To retrieve the actual heap pointer, we need to get the tagged
    // heap pointer and remove the tag.
    int64_t* object_ptr = gc_remove_ptr_tag(*object_ptr_ptr);
    /* printf_if_debug("  OBJ PTR: %" PRIu64 "\n", (uint64_t) *object_ptr_ptr); */
    /* printf_if_debug("  OBJ PTR: %" PRIu64 "\n", (uint64_t) object_ptr); */

    // Check if the meta data has the forwarding bit set
    if (gc_is_forwarded(object_ptr)) {
      printf_if_debug("  heap ptr: object already copied\n");
      // In this case, the meta data is the forwarding pointer with the
      // tag bit set to 1. We do not need to set the tag bit to 0,
      // because we need to store a tagged pointer anyways (the tag now
      // just means "heap ptr" instead of "forwarded").
      *object_ptr_ptr = (int64_t*) *object_ptr;
    } else {
      // In this case, the meta data contains the number of words after
      // the meta data.  We rightshift to remove the 0 tag bit, and add
      // 1 to account for the meta data itself.
      uint64_t word_len = 1 + (((uint64_t) *object_ptr) >> 1);

      printf_if_debug("  heap ptr: copying object of %" PRIu64 " words...\n", word_len);
      /* printf_if_debug("    %d\n", (object_ptr < gc_fromspace_end && object_ptr >= gc_fromspace_begin)); */
      /* printf_if_debug("    %d\n", object_ptr); */

      // Copy all the bytes of the object
      int64_t* new_object_ptr = gc_free_ptr;
      uint64_t num_bytes = word_len * 8;
      memcpy(new_object_ptr, object_ptr, num_bytes);

      // Add forwarding pointer to old object.
      *object_ptr = (uint64_t) gc_add_ptr_tag(new_object_ptr);

      // Move the free_ptr up by how many bytes we used.
      gc_free_ptr += word_len;

      // Adjust the pointer, which previously pointed to the
      // from-space object, to point to the new to-space object.
      // Note that we need to add a tag to new_object_ptr,
      // because it is also a heap pointer.
      *object_ptr_ptr = gc_add_ptr_tag(new_object_ptr);
    }
  } else {
    printf_if_debug("  no heap ptr of value: %" PRIu64 "\n", *p >> 1);
      /* printf_if_debug("    %" PRIu64 "\n", (uint64_t) (gc_stack_begin - p)); */
  }
}

void gc_copy_and_swap_spaces(
  int64_t* stack_end
) {
  printf_if_debug("from begin: %d\n", gc_fromspace_begin);
  printf_if_debug("from end:   %d\n", gc_fromspace_end);
  printf_if_debug("free_ptr:   %d\n", gc_free_ptr);

  gc_free_ptr = gc_tospace_begin;

  printf_if_debug("Scanning stack...\n");
  // Stack grows upwards!
  for (int64_t* p = gc_stack_begin - 1; p >= stack_end; --p) {
    gc_copy_if_heap_ptr(p);
  }

  printf_if_debug("Scanning to-space...\n");
  // Note that gc_free_ptr in the for-loop condition might
  // increase while the for-loop is running due to the calls to
  // gc_copy_object. This is by design!
  for (int64_t* p = gc_tospace_begin; p < gc_free_ptr; ++p) {
    gc_copy_if_heap_ptr(p);
  }

  // Swap from-space and to-space
  int64_t* tmp_begin = gc_fromspace_begin;
  int64_t* tmp_end = gc_fromspace_end;
  gc_fromspace_begin = gc_tospace_begin;
  gc_fromspace_end = gc_tospace_end;
  gc_tospace_begin = tmp_begin;
  gc_tospace_end = tmp_end;
}

void gc_collect(
  int64_t* stack_end,
  uint64_t requested_words
) {
  printf_if_debug("\n–––––––––– gc_collect ––––––––––\n");

  // Copy from-space to to-space and swap
  gc_copy_and_swap_spaces(stack_end);

  // If garbage collection did not free enough memory, reallocate
  // from- and to-space.
  if (gc_free_ptr + requested_words >= gc_fromspace_end) {
    // Compute new space size
    uint64_t cur_space_words = gc_fromspace_end - gc_fromspace_begin;
    uint64_t new_space_words = cur_space_words;
    while (new_space_words < cur_space_words + requested_words) {
      new_space_words *= 2;
    }
    printf_if_debug("Reallocating spaces:\n");
    printf_if_debug("  requested words:      %" PRId64 "\n", requested_words);
    printf_if_debug("  current space words:  %" PRId64 "\n", cur_space_words);
    printf_if_debug("  new space words:      %" PRId64 "\n", new_space_words);

    // Reallocate to-space
    free(gc_tospace_begin);
    gc_tospace_begin = malloc(new_space_words * 8);
    gc_tospace_end = gc_tospace_begin + new_space_words;

    // Copy from-space to to-space and swap
    gc_copy_and_swap_spaces(stack_end);

    // Reallocate to-space
    free(gc_tospace_begin);
    gc_tospace_begin = malloc(new_space_words * 8);
    gc_tospace_end = gc_tospace_begin + new_space_words;
  }
  printf_if_debug("––––––––––––––––––––––––––––––––\n");
} 

// Tests ///////////////////////////////////////////////////////////////////////

// int64_t* fake_stack_begin;
// int64_t* fake_stack_cur;
// int64_t* fake_stack_end;
// 
// uint64_t next_element = 10000;
// 
// int64_t* alloc_tuple(uint64_t num_elements) {
//   printf_if_debug("\nAllocating tuple with %" PRIu64 " elements...\n", num_elements);
//   uint64_t num_words = num_elements + 1;
//   if (gc_free_ptr + num_words >= gc_fromspace_end) {
//     gc_collect(fake_stack_cur, num_words);
//   }
//   int64_t* t = gc_free_ptr;
//   gc_free_ptr += num_words;
//   t[0] = num_elements << 1;
//   for (uint64_t i = 0; i < num_elements; ++i) {
//     t[i+1] = (next_element + i) << 1;
//   }
//   next_element += 100;
//   return gc_add_ptr_tag(t);
// }
// 
// int main() {
//   uint64_t stack_size = 1024;
//   uint64_t heap_size = 8;
// 
//   int64_t* begin = malloc(stack_size * 8);
//   int64_t* end = begin + stack_size;
//   fake_stack_end = begin;
//   fake_stack_begin = end;
//   fake_stack_cur = fake_stack_begin;
// 
//   gc_init(fake_stack_begin, heap_size);
// 
//   for (uint64_t i = 0; i < 5; ++i) {
//     *(fake_stack_cur--) = i << 1; 
//   }
// 
//   for (uint64_t i = 0; i < 5; ++i) {
//     *(fake_stack_cur--) = (int64_t) alloc_tuple(2);
//   }
// }
