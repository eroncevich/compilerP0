.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $20, %esp
	movl $5, %eax
	movl $1, %eax
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %edi
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %esi
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %ebx
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, -8(%ebp)
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, -20(%ebp)
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, -4(%ebp)
	call create_dict
	addl $0, %esp
	movl %eax,-12(%ebp)
	pushl -12(%ebp)
	call inject_big
	addl $4, %esp
	movl %eax,-16(%ebp)
	pushl %edi
	pushl %esi
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl %ebx
	pushl -8(%ebp)
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl -20(%ebp)
	pushl -4(%ebp)
	pushl -16(%ebp)
	call set_subscript
	addl $12, %esp
	pushl -12(%ebp)
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $0,%eax
	leave
	ret
