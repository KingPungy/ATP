.cpu cortex-m0
.align 2

.text
.global greater

greater:
push { r4, r5, r6, lr }
mov r4, r0
mov r5, r1
mov r6, #0
whileBegin_f00782ef01:
mov r0, r4
mov r1, #0
cmp r0, r1
beq whileEnd_f00782ef01
mov r0, #1
sub r4, r4, r0
mov r0, r4
mov r1, r5
cmp r0, r1
bne ifEnd_0b1f992199
mov r0, #1
add r6, r6, r0
ifEnd_0b1f992199:
b whileBegin_f00782ef01
whileEnd_f00782ef01:
mov r0, r6
pop { r4, r5, r6, pc }
