.cpu cortex-m0
.align 2

.text
.global power

power:
push { r4, r5, r6, lr }
mov r4, r0
mov r5, r1
mov r6, #1
whileBegin_efe7210309:
mov r0, r5
mov r1, #0
cmp r0, r1
beq whileEnd_efe7210309
mul r6, r6, r4
mov r0, #1
sub r5, r5, r0
b whileBegin_efe7210309
whileEnd_efe7210309:
mov r0, r6
pop { r4, r5, r6, pc }
