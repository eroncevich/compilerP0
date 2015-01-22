.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $8, %esp
	call input
	movl %eax, -4(%ebp)
	movl -4(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -8(%ebp), %eax
	pushl %eax
	call print_int_nl
	popl %eax
	movl $0,%eax
	leave
	ret
