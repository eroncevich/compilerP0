.globl main
main:
  pushl %ebp
  movl %esp, %ebp
  subl $4, %esp
  movl $2,-4(%ebp)
  movl -4(%ebp),%eax
  leave
  ret
