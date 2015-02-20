.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $1, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $2, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $3, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	pushl %eax
	call input
	movl %eax, %eax
	movl %eax, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $5, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $6, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $0,%eax
	leave
	ret
