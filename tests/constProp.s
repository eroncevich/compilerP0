.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $5, %eax
	movl $1, %eax
	movl $8, %ebx
	movl $12, %eax
	movl %ebx, %ebx
	sarl $2, %ebx
	movl %eax, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	movl $0,%eax
	leave
	ret
