.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $4, %esp
	pushl $1
	call inject_int
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call create_list
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%esi
	pushl $0
	call inject_int
	addl $4, %esp
	movl %eax,%edi
	pushl $31111108
	pushl %edi
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ebx
	movl $5, %eax
	movl $1, %eax
	movl $28, %esi
	pushl %esi
	pushl $0
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	addl $4, %esp
	movl %eax,%edi
	pushl %edi
	call create_list
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call inject_big
	addl $4, %esp
	movl %eax,%edi
	pushl $0
	call inject_int
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl %ebx
	pushl -4(%ebp)
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl %esi
	call inject_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	pushl $testa0
	call create_closure
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %esi
	pushl %esi
	call get_free_vars
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %esi
	call get_fun_ptr
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ecx
	pushl %ebx
	pushl %esi
	pushl %edi
	pushl %ebx
	call *%ecx
	addl $4, %esp
	popl %edi
	popl %esi
	popl %ebx
	movl %eax,%eax
	movl %eax, %eax
	movl $0,%eax
	leave
	ret
testa0:
	pushl %ebp
	movl %esp, %ebp
	pushl $0
	pushl 8(%ebp)
	call get_subscript
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %esi
	pushl $0
	pushl %esi
	call get_subscript
	addl $8, %esp
	movl %eax,%ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $0,%eax
	leave
	ret
