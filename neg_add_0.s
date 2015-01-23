.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $12, %esp
	movl $2,-4(%ebp)
	movl $1, %eax
	addl -4(%ebp), %eax
	movl %eax, -8(%ebp)
	movl -8(%ebp), %eax
	negl %eax
	movl %eax, -12(%ebp)
	movl -12(%ebp), %eax
	pushl %eax
	call print_int_nl
	popl %eax
	movl $0,%eax
	leave
	ret
