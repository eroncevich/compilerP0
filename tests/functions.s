.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $5, %eax
	movl $1, %eax
	pushl %ebx
	call test
	movl %eax,%eax
	addl $4, %esp
	movl %eax, %eax
	movl $0,%eax
	leave
	ret
