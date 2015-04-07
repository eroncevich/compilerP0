.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $5, %eax
	movl $1, %eax
	movl $4, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $8, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $12, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $20, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $24, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $0,%eax
	leave
	ret
