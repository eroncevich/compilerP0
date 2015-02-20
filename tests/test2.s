.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $24, %esp
	movl $1, -20(%ebp)
	movl $2, -16(%ebp)
	movl $3, -24(%ebp)
	pushl %eax
	call input
	movl %eax, %eax
	movl %eax, %eax
	movl $5, %eax
	movl $6, -12(%ebp)
	movl $7, %edi
	movl $8, %eax
	movl $9, %eax
	movl $10, %esi
	movl $11, -4(%ebp)
	movl $12, -8(%ebp)
	pushl -20(%ebp)
	call print_int_nl
	popl -20(%ebp)
	movl -20(%ebp), %eax
	addl -12(%ebp), %eax
	movl %eax, %eax
	addl -16(%ebp), %eax
	movl %eax, %eax
	addl %edi, %eax
	movl %eax, %eax
	addl -24(%ebp), %eax
	movl %eax, %eax
	addl -16(%ebp), %eax
	movl %eax, %eax
	addl %edi, %eax
	movl %eax, -16(%ebp)
	pushl %eax
	call input
	movl %eax, %eax
	movl %eax, %edi
	movl -16(%ebp), %eax
	addl %edi, %eax
	movl %eax, %eax
	addl -24(%ebp), %eax
	movl %eax, %eax
	addl %esi, %eax
	movl %eax, %eax
	addl -4(%ebp), %eax
	movl %eax, %eax
	addl -8(%ebp), %eax
	movl %eax, -24(%ebp)
	movl -16(%ebp), %eax
	addl -20(%ebp), %eax
	movl %eax, -24(%ebp)
	movl -24(%ebp), %eax
	movl %eax, -20(%ebp)
	pushl -24(%ebp)
	call print_int_nl
	popl -24(%ebp)
	movl $0,%eax
	leave
	ret
