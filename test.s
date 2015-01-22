.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $80, %esp
	movl $1,-4(%ebp)
	movl $4,-8(%ebp)
	movl $1, %eax
	addl -4(%ebp), %eax
	movl %eax, -12(%ebp)
	movl -12(%ebp), %eax
	addl $5, %eax
	movl %eax, -16(%ebp)
	movl -16(%ebp),%eax
	movl %eax,-20(%ebp)
	movl -8(%ebp), %eax
	addl $1, %eax
	movl %eax, -24(%ebp)
	movl -24(%ebp),%eax
	movl %eax,-8(%ebp)
	movl $4,-4(%ebp)
	movl $4,-8(%ebp)
	movl $4,-20(%ebp)
	movl -20(%ebp), %eax
	negl %eax
	movl %eax, -28(%ebp)
	movl -28(%ebp),%eax
	movl %eax,-20(%ebp)
	call input
	movl %eax, -32(%ebp)
	movl -32(%ebp), %eax
	addl -4(%ebp), %eax
	movl %eax, -36(%ebp)
	movl -36(%ebp), %eax
	addl $1, %eax
	movl %eax, -40(%ebp)
	movl -40(%ebp),%eax
	movl %eax,-8(%ebp)
	movl -4(%ebp), %eax
	pushl %eax
	call print_int_nl
	popl %eax
	movl -8(%ebp), %eax
	pushl %eax
	call print_int_nl
	popl %eax
	movl -4(%ebp), %eax
	addl $1, %eax
	movl %eax, -44(%ebp)
	movl -44(%ebp), %eax
	addl -8(%ebp), %eax
	movl %eax, -48(%ebp)
	movl -48(%ebp), %eax
	pushl %eax
	call print_int_nl
	popl %eax
	movl $-1, -52(%ebp)
	movl -20(%ebp), %eax
	addl -52(%ebp), %eax
	movl %eax, -56(%ebp)
	movl -56(%ebp), %eax
	pushl %eax
	call print_int_nl
	popl %eax
	movl $0,%eax
	leave
	ret
