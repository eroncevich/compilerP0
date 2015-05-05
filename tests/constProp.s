.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $5, %eax
	movl $1, %eax
	movl $4, %eax
	movl $4, %eax
	movl $4, %eax
	movl $4, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $0,%eax
	leave
	ret
