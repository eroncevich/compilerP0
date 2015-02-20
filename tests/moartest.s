.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	movl $3, %esi
	pushl %esi
	call print_int_nl
	popl %esi
	movl $1, %esi
	pushl %eax
	call input
	movl %eax, %eax
	movl $1, %ebx
	movl $0, %eax
	addl %ebx, %eax
	movl %eax, %eax
	addl %esi, %eax
	movl %eax, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $1, %eax
	addl %ebx, %eax
	movl %eax, %eax
	movl $2, %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl %esi, %ebx
	negl %ebx
	pushl %ebx
	call print_int_nl
	popl %ebx
	movl $0,%eax
	leave
	ret
