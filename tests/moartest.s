.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $16, %esp
	movl $5, %eax
	movl $1, %eax
	movl $4, %edi
	movl $8, %esi
	movl %edi, %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then0
	movl %edi, %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then1
	movl $777777, %eax
	jmp end1
	then1:
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %esi
	call project_big
	addl $4, %esp
	movl %eax,%edi
	pushl %edi
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end1:
	movl %eax, %eax
	jmp end0
	then0:
	movl %edi, %eax
	sarl $2, %eax
	movl %esi, %ecx
	sarl $2, %ecx
	movl %eax, %ebx
	addl %ecx, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end0:
	movl %eax, %eax
	movl %eax, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $4, %esi
	call input_int
	addl $0, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl $4, %edi
	movl $4, -4(%ebp)
	movl $4, %ebx
	movl %ebx, %ecx
	andl $3, %ecx
	cmp $0, %ecx
	movl $1, %ecx
	movl $0, %eax
	cmove %ecx, %eax
	pushl %eax
	call inject_bool
	addl $4, %esp
	movl %eax,%eax
	movl %eax, -8(%ebp)
	pushl -8(%ebp)
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, -12(%ebp)
	pushl -12(%ebp)
	call inject_bool
	addl $4, %esp
	movl %eax,-16(%ebp)
	pushl -16(%ebp)
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then2
	movl %ebx, %ecx
	andl $3, %ecx
	cmp $1, %ecx
	movl $1, %ecx
	movl $0, %eax
	cmove %ecx, %eax
	pushl %eax
	call inject_bool
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	jmp end2
	then2:
	movl -8(%ebp), %eax
	end2:
	movl %eax, -8(%ebp)
	pushl -8(%ebp)
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then3
	movl $777777, %eax
	jmp end3
	then3:
	movl %ebx, %eax
	sarl $2, %eax
	movl %eax, %ebx
	negl %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end3:
	movl %eax, %eax
	movl %eax, -8(%ebp)
	movl -4(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then4
	movl -4(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then5
	movl $777777, %eax
	jmp end5
	then5:
	pushl -4(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl -8(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl -4(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end5:
	movl %eax, %eax
	jmp end4
	then4:
	movl -4(%ebp), %ebx
	sarl $2, %ebx
	movl -8(%ebp), %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end4:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -4(%ebp)
	movl %edi, %edi
	movl -4(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then6
	movl -4(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then7
	movl $777777, %eax
	jmp end7
	then7:
	pushl -4(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl -4(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end7:
	movl %eax, %eax
	jmp end6
	then6:
	movl -4(%ebp), %ebx
	sarl $2, %ebx
	movl %edi, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end6:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, -4(%ebp)
	movl %esi, %edi
	movl -4(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then8
	movl -4(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then9
	movl $777777, %eax
	jmp end9
	then9:
	pushl -4(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl -4(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end9:
	movl %eax, %eax
	jmp end8
	then8:
	movl -4(%ebp), %ebx
	sarl $2, %ebx
	movl %edi, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end8:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, %edi
	pushl %edi
	call print_any
	popl %edi
	movl $4, -4(%ebp)
	movl %edi, %edi
	movl -4(%ebp), %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then10
	movl -4(%ebp), %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then11
	movl $777777, %eax
	jmp end11
	then11:
	pushl -4(%ebp)
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl -4(%ebp)
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end11:
	movl %eax, %eax
	jmp end10
	then10:
	movl -4(%ebp), %ebx
	sarl $2, %ebx
	movl %edi, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end10:
	movl %eax, %eax
	movl %eax, %eax
	movl %eax, %eax
	movl $8, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl %esi, %ebx
	movl %ebx, %ecx
	andl $3, %ecx
	cmp $0, %ecx
	movl $1, %ecx
	movl $0, %eax
	cmove %ecx, %eax
	pushl %eax
	call inject_bool
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %esi
	pushl %esi
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, -4(%ebp)
	pushl -4(%ebp)
	call inject_bool
	addl $4, %esp
	movl %eax,%edi
	pushl %edi
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then12
	movl %ebx, %ecx
	andl $3, %ecx
	cmp $1, %ecx
	movl $1, %ecx
	movl $0, %eax
	cmove %ecx, %eax
	pushl %eax
	call inject_bool
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	jmp end12
	then12:
	movl %esi, %eax
	end12:
	movl %eax, %esi
	pushl %esi
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then13
	movl $777777, %eax
	jmp end13
	then13:
	movl %ebx, %eax
	sarl $2, %eax
	movl %eax, %ebx
	negl %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end13:
	movl %eax, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $0,%eax
	leave
	ret
