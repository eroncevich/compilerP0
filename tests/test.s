.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $36, %esp
	movl $1, -24(%ebp)
	movl $2, -20(%ebp)
	movl $3, -28(%ebp)
	pushl %eax
	call input
	movl %eax, %eax
	movl %eax, -36(%ebp)
	movl $5, -32(%ebp)
	movl $6, -16(%ebp)
	movl $7, %edi
	movl $8, %esi
	movl $9, %eax
	movl $10, -8(%ebp)
	movl $11, -4(%ebp)
	movl $12, -12(%ebp)
	pushl -24(%ebp)
	call print_int_nl
	popl -24(%ebp)
	movl -24(%ebp), %eax
	addl -20(%ebp), %eax
	movl %eax, %eax
	addl -28(%ebp), %eax
	movl %eax, %eax
	addl -36(%ebp), %eax
	movl %eax, %eax
	addl -32(%ebp), %eax
	movl %eax, %eax
	addl -16(%ebp), %eax
	movl %eax, %eax
	addl %edi, %eax
	movl %eax, %eax
	addl %esi, %eax
	movl %eax, %eax
	addl -24(%ebp), %eax
	movl %eax, %eax
	addl -32(%ebp), %eax
	movl %eax, %eax
	addl -20(%ebp), %eax
	movl %eax, %eax
	addl -36(%ebp), %eax
	movl %eax, %esi
	negl %esi
	pushl %esi
	call print_int_nl
	popl %esi
	movl -24(%ebp), %eax
	addl -16(%ebp), %eax
	movl %eax, %eax
	addl -20(%ebp), %eax
	movl %eax, %eax
	addl %edi, %eax
	movl %eax, %eax
	addl -28(%ebp), %eax
	movl %eax, %eax
	addl -20(%ebp), %eax
	movl %eax, %eax
	addl %edi, %eax
	movl %eax, -20(%ebp)
	pushl %eax
	call input
	movl %eax, %eax
	movl %eax, %edi
	movl -20(%ebp), %eax
	addl %edi, %eax
	movl %eax, %eax
	addl -28(%ebp), %eax
	movl %eax, %eax
	addl -8(%ebp), %eax
	movl %eax, %eax
	addl -4(%ebp), %eax
	movl %eax, %eax
	addl -12(%ebp), %eax
	movl %eax, -28(%ebp)
	movl -20(%ebp), %eax
	addl -24(%ebp), %eax
	movl %eax, -28(%ebp)
	movl -28(%ebp), %eax
	movl %eax, -24(%ebp)
	pushl -28(%ebp)
	call print_int_nl
	popl -28(%ebp)
	movl $0,%eax
	leave
	ret
